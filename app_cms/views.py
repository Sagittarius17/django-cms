from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.hashers import make_password, check_password

def index_view(request):
    return render ( request , 'base.html' )

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = SimpleUser.objects.get(username=username)
            
            if check_password(password, user.password):
                # You need to set up your own login logic if you're not using Django's built-in User model
                # For now, I'm leaving it as a comment, but you might want to implement sessions or some other way.
                # login(request, user)
                return redirect('article_list')  # or wherever you want to redirect after login
            else:
                # Password does not match
                pass
        except SimpleUser.DoesNotExist:
            # Username does not exist
            pass
        
        # handle error, e.g., show a message to the user
        # You might want to add an error message here to inform the user

    return render(request, 'app_cms/login.html')

def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        
        if password == confirm_password:
            # IMPORTANT: Always hash the password before storing!
            hashed_password = make_password(password)
            
            user = SimpleUser(username=username, email=email, password=hashed_password)
            user.save()
            return redirect('login')
        else:
            pass
    return render(request, 'app_cms/register.html')

def logout_view(request):
    logout(request)
    return redirect('login')


def article_list(request):
    articles = Article.objects.all()
    return render(request, 'app_cms/article_list.html', {'articles': articles})

def article_detail(request, pk):
    article = Article.objects.get(pk=pk)
    return render(request, 'app_cms/article_detail.html', {'article': article})