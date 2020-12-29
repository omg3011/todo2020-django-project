from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm      # For Sign-up form
from django.db import IntegrityError                        # For handling error: username already taken
from django.contrib.auth.models import User                 # For retrieving signup authentication data which user input
from .forms import CreateUserForm, TodoForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Todo
from django.utils import timezone

# Intro Page
def index(request):
    return render(request, 'todo/index2.html')

# Home Page
@login_required(login_url='login')
def home(request):
    # Filter according to user
    todos = Todo.objects.filter(user=request.user, datecompleted__isnull=True, archieve=False) # Only want objects that's no completed Yet
    context = {'todos':todos}
    return render(request, 'todo/home.html', context)

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

# Logout
def logoutuser(request):
    logout(request)
    return redirect('loginuser')


# Completed Page
@login_required(login_url='login')
def completedtodos(request):
    # Filter according to user
    todos = Todo.objects.filter(user=request.user, datecompleted__isnull=False, archieve=False) # Only want objects that's no completed Yet
    context = {'todos':todos}
    return render(request, 'todo/home.html', context)

# Archieve Page
@login_required(login_url='login')
def archievedtodos(request):
    # Filter according to user
    todos = Todo.objects.filter(user=request.user, archieve=True) # Only want objects that's no completed Yet
    context = {'todos':todos}
    return render(request, 'todo/home.html', context)


# CreateToDo page
@login_required(login_url='login')
def createtodo(request):
    form = TodoForm()

    # Display ToDo form
    if request.method == 'GET':
        return render(request, 'todo/createtodo.html', {'form': form})
    # Process ToDo form
    else:
        # Attempt to process form s
        try:
            form = TodoForm(request.POST)     # Retrieve user input from the form he just input-ed
            newtodo = form.save(commit=False)
            newtodo.user = request.user
            newtodo.save()
            return redirect('home')
        # Failed to process form due to too much characters
        except ValueError:
            return render(request, 'todo/createtodo.html', 'error', 'You typed too much characters.')

# ViewTodo page
@login_required(login_url='login')
def viewtodo(request, todo_pk):
    # user = retrieve this user, check if this user got todo
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    # Display ViewToDoPage
    if request.method == 'GET':
        form = TodoForm(instance=todo)
        return render(request, 'todo/ViewTodo.html', {'todo':todo, 'form':form})
    # Modified ViewToDoPage
    else:
        try:
            form = TodoForm(request.POST, instance=todo) #instance=todo will tell them we are reusing same user
            form.save()
            return redirect('home')
        except ValueError:
            return render(request, 'todo/viewtodo.html', {'todo':todo, 'form':form, 'error': 'You typed too much characters.'})


# Button: Completetodo
@login_required(login_url='login')
def btn_completetodo(request, todo_pk):
    # user = retrieve this user, check if this user got todo
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.datecompleted = timezone.now()
        todo.save()
        return redirect('home')

# Button: Deletetodo
@login_required(login_url='login')
def btn_deletetodo(request, todo_pk):
    # user = retrieve this user, check if this user got todo
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.delete()
        return redirect('home')

# Button: Archievetodo
@login_required(login_url='login')
def btn_archievetodo(request, todo_pk):
    # user = retrieve this user, check if this user got todo
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.archieve = True
        todo.save()
        return redirect('home')
