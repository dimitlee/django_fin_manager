from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

from .forms import SignupForm, LoginForm


def user_signup(request, next=None):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password1 = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']
            user = authenticate(request, username=username, password=password1)
            if user:
                login(request, user)
            if next:
                return redirect(next)
            else:
                return redirect('index')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})


def user_login(request, next=None):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
            if next:
                return redirect(next)
            else:
                return redirect('index')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})
    
    
def user_logout(request):
    logout(request)
    return redirect('login')