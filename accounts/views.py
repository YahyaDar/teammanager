from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import RegisterForm, LoginForm


def login_user(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                messages.error(request, "There was an error logging in, try again.")
                return redirect('login')
    else:
        form = LoginForm()

    return render(request, 'register/login.html', {'form': form})


def logout_user(request):
    logout(request)
    messages.success(request, "You were logged out!")
    return redirect('index')


def register_user(request):
    if request.method == "POST":
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            user = authenticate(username=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Registration successful!")
                return redirect('index')
    else:
        form = RegisterForm()

    return render(request, 'register/register_user.html', {'form': form})


def index(request):
    return render(request, 'register/index.html')
