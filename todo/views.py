from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm      # For Sign-up form
from django.db import IntegrityError                        # For handling error: username already taken
from django.contrib.auth.models import User                 # For retrieving signup authentication data which user input
from .forms import CreateUserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Home Page
def index(request):
    return render(request, 'todo/index.html')

# Signup Page
def signupuser(request):
    # If login already, go to home page
    if request.user.is_authenticated:
        return redirect('home')

    # Else if not login-ed
    else:
        # Create a new register form
        form = CreateUserForm()

        # User clicked on register account button
        if request.method == 'POST':
            # Fill it up with the data user input-ed
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for ' + user)
                return redirect('loginuser')

        context = {'form': form}
        return render(request, 'todo/signupuser.html', context)

# Login Page
def loginuser(request):
    # If login already, go to home Page
    if request.user.is_authenticated:
        return redirect('home')
    # Else if not login-ed
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            # If success in login, redirect to home page
            if user is not None:
                login(request,user)
                return redirect('home')
            # If failed in login, print Error Messageg
            else:
                messages.info(request, 'Username OR password is incorrect')
        context = {}
        return render(request, 'todo/loginuser.html', context)

# Logout Page
def logoutuser(request):
    logout(request)
    return redirect('loginuser')



@login_required(login_url='login')
def home(request):
    return render(request, 'todo/home.html')
