from typing import Any
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
from django.http import Http404
from django.urls import reverse

from .models import Category, Transaction
from .forms import TransactionForm, CategoryForm, ScheduledTransactionForm


class DefaultLoginRequiredMixin(LoginRequiredMixin):
    login_url = 'login'


class UserCategoryListView(DefaultLoginRequiredMixin, ListView):
    model = Category
    template_name = 'index.html'
    
    def get_queryset(self) -> QuerySet[Any]:
        user_categories = Category.objects.filter(user=self.request.user)
        
        annotated_categories = user_categories.annotate(
            total_spent = Coalesce(Sum('transaction__sum'), 0)
        )
        
        return annotated_categories
    

class UserCategoryDetailView(DefaultLoginRequiredMixin, DetailView):
    model = Category
    
    def get_object(self, queryset: QuerySet[Any] | None = None) -> Model:
        category = super().get_object(queryset)
        
        if not category or category.user != self.request.user:
            raise Http404("Category not found or it does not belong to you")
        
        return category
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['transaction_form'] = TransactionForm(
            user=self.request.user, 
            category=self.object
        )
        return context
    

class CategoryToAddListView(DefaultLoginRequiredMixin, ListView):
    model = Category
    template_name = 'finances/category_to_add_list.html'
    
    @property
    def user_categories(self):
        if not hasattr(self, '_user_categories'):
            self._user_categories = Category.objects.filter(user=self.request.user)
        return self._user_categories
    
    def get_queryset(self) -> QuerySet[Any]:
        default_categories = Category.objects.filter(user=None)
        user_categories_names = set(self.user_categories.values_list('name', flat=True))
        
        for category in default_categories:
            category.is_added_by_user = category.name in user_categories_names
        
        return default_categories
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["user_categories"] = self.user_categories
        return context
    

@login_required(login_url='login')
def add_category(request, pk):
    category = Category.objects.get(id=pk)
    new_category = Category(
        name=category.name,
        description=category.description,
        user=request.user
    )
    new_category.save()
    return redirect('my-categories')


@login_required(login_url='login')
def create_category(request, next=None):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user
            category.save()
            return redirect(next or 'my-categories')
    else:
        form = CategoryForm()
    
    return render(request, 'forms/create_category.html', {'form': form})


@login_required(login_url='login')
def create_transaction(request):
    next = request.GET.get('next')
    if request.method == 'POST':
        form = TransactionForm(request.POST, user=request.user)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            if form.cleaned_data['add_schedule']:
                request.session['scheduled_transaction_data'] = {
                    'description': form.cleaned_data['description'],
                    'sum': form.cleaned_data['sum'],
                    'category': form.cleaned_data['category'].id,
                }
                return redirect('create-scheduled-transaction')
            else:
                return redirect(next or 'index')
    else:
        form = TransactionForm(user=request.user)
        
    return render(request, 'forms/create_transaction.html', {'form': form})


@login_required(login_url='login')
def delete_transaction(request, pk, next=None):
    transaction = Transaction.objects.get(id=pk)
    transaction.delete()
    return redirect(next or 'index')


@login_required(login_url='login')
def create_scheduled_transaction(request):
    next = request.GET.get('next')
    scheduled_transaction_data = request.session.pop('scheduled_transaction_data', None)
    initial = None
    if scheduled_transaction_data:
        initial={
            'description': scheduled_transaction_data['description'],
            'sum': scheduled_transaction_data['sum'],
            'category': scheduled_transaction_data['category']
        }
    if request.method == 'POST':
        form = ScheduledTransactionForm(request.POST, user=request.user)
        if form.is_valid():
            sch_transaction = form.save(commit=False)
            sch_transaction.user = request.user
            sch_transaction.save()
            return redirect(next or 'index')
    else:
        form = ScheduledTransactionForm(initial=initial, user=request.user)
    
    return render(request, 'forms/create_scheduled_transaction.html', {'form': form, 'next': next})
            