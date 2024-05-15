from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required

# Create your views here.


def home(request):
    """
    The main view of the system
    """
    return render(request, 'home.html')


@login_required
def expenses(request):
    """
    List of expenses of the user
    """
    return render(request, 'expenses.html')


@login_required
def incomes(request):
    """
    List of incomes of the user
    """
    return render(request, 'incomes.html')


@login_required
def report(request):
    """
    General report of expenses and incomes
    """
    return render(request, 'report.html')


# user views
def register_user(request):
    """
    GET - Shows the register form to the user
    POST - Register a new user in system
    """
    # GET METHOD
    if request.method == 'GET':
        return render(request, 'register.html')
    # POST METHOD
    else:
        error = ""
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        # The passwords match
        if password1 == password2:
            # Create a new user in db
            try:
                user = User.objects.create_user(
                    username=username,
                    password=password1
                )
                user.save()
                login(request, user)
                return redirect('report')
            # The user already exists in db
            except IntegrityError:
                error = "The user already exists"
        # Passwords do not match
        else:
            error = "Passwords do not match"

        return render(request, 'register.html', {
            'error': error
        })


def login_user(request):
    """
    GET - Shows the login form to the user
    POST - Login in to system
    """
    # GET METHOD
    if request.method == 'GET':
        return render(request, 'login.html')
    # POST METHOD
    else:
        error = ""
        username = request.POST['username']
        password = request.POST['password']

        # verify if the user exists in db
        user = authenticate(request, username=username, password=password)

        # user is valid
        if user is not None:
            # login system
            login(request, user)
            return redirect('report')
        # user is not valid
        else:
            error = "Username or password are incorrect"
            return render(request, 'login.html', {
                'error': error
            })


@login_required
def logout_user(request):
    """
    Logout the user from the system
    """
    logout(request)
    return redirect('home')
