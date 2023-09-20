from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect
from .models import *

def index_view(request):
    return render ( request , 'base.html' )

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('article_list')
    else:
        form = UserCreationForm()
    return render(request, 'content/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('article_list')
    else:
        form = AuthenticationForm()
    return render(request, 'content/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login_view')


def article_list(request):
    articles = Article.objects.all()
    return render(request, 'content/article_list.html', {'articles': articles})

def article_detail(request, pk):
    article = Article.objects.get(pk=pk)
    return render(request, 'content/article_detail.html', {'article': article})