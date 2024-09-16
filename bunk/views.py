from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from .models import Bunk, User
from .forms import BunkForm, UserRegistrationForm, UserLoginForm
from django.contrib.auth import authenticate, login
from django.contrib import messages

# Create your views here.
def main_feed(request):
    form = BunkForm()
    bunks = Bunk.objects.all()
    
    if request.method == 'POST':
        form = BunkForm(request.POST)
        if form.is_valid():
            form.save()
        
    return render(request, 'bunk/main_feed.html', {'bunks': bunks, 'form': form})

def personal_feed(request, username):
    if not request.user.is_authenticated or request.user.username != username:
        raise Http404("User does not exist or is not logged in.")
    
    form = BunkForm()
    
    if request.method == 'POST':
        form = BunkForm(request.POST)
        if form.is_valid():
            form.save()
    
    bunks_received = Bunk.objects.filter(to_user=request.user)
    bunks_sent = Bunk.objects.filter(from_user=request.user)
    
    return render(request, 'bunk/personal_feed.html', {'bunks_received': bunks_received, 'bunks_sent': bunks_sent, 'user': request.user, 'form': form})

def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome, {user.username}!")
                return redirect('/user/' + user.username)
            else:
                messages.error(request, 'Invalid username or password')
    else:
        form = UserLoginForm()
    
    return render(request, 'bunk/login.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()  # No need to set the password manually
            login(request, user)  # Automatically log the user in after registration
            messages.success(request, f"Account created for {user.username}!")
            return redirect('/user/' + user.username)  # Redirect to personal page after successful registration
    else:
        form = UserRegistrationForm()
    
    return render(request, 'bunk/register.html', {'form': form})