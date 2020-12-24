from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm      # For Sign-up form
from django.db import IntegrityError                        # For handling error: username already taken
from django.contrib.auth.models import User                 # For retrieving signup authentication data which user input


# Home Page
def index(request):
    return render(request, 'todo/index.html')

# Signup Page
def signupuser(request):
    form = UserCreationForm()

    if request.method == 'POST':
        if form.is_valid():
            form.save()

    context = {'form': form}

    return render(request, 'todo/signupuser.html', context)

# Login Page
def loginuser(request):
    return render(request, 'todo/loginuser.html')

# Logout Page
def logoutuser(request):
    return render(request, 'todo/index.html')
