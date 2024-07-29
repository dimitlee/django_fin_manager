from django import forms
from django.utils import timezone
import datetime

from .models import Category, Transaction, ScheduledTransaction


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']
    
    
class TransactionForm(forms.ModelForm):
    add_schedule = forms.BooleanField(required=False, label="Schedule this transaction?")
    fields_class = "transaction_field"
    
    class Meta:
        model = Transaction
        fields = ['category', 'description', 'sum', 'time']
        
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        category = kwargs.pop('category', None)
        super(TransactionForm, self).__init__(*args, **kwargs)
        self.fields['time'].initial = timezone.now()
        if category:
            self.fields['category'].queryset = Category.objects.filter(id=category.id)
            self.fields['category'].initial = category
        elif user:
            self.fields['category'].queryset = Category.objects.filter(user=user)
        for field_name in self.fields:
            field = self.fields.get(field_name)
            field.widget.attrs['id'] = f"transaction_{field_name}"
            field.widget.attrs['class'] = self.fields_class
            

class ScheduledTransactionForm(forms.ModelForm):
    fields_class = "scheduled_transaction_field"
    
    class Meta:
        model = ScheduledTransaction
        fields = ['category', 'description', 'sum', 'frequency', 'weekday', 'monthday', 'year_date']
        
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        category = kwargs.pop('category', None)
        super(ScheduledTransactionForm, self).__init__(*args, **kwargs)
        today = datetime.date.today()
        self.fields['weekday'].initial = today.weekday()
        self.fields['monthday'].initial = today.day
        self.fields['year_date'].initial = today
        if category:
            self.fields['category'].queryset = Category.objects.filter(id=category.id)
            self.fields['category'].initial = category
        elif user:
            self.fields['category'].queryset = Category.objects.filter(user=user)
        for field_name in self.fields:
            field = self.fields.get(field_name)
            field.widget.attrs['id'] = f"scheduled_transaction_{field_name}"
            field.widget.attrs['class'] = self.fields_class