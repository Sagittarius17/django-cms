from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.hashers import make_password, check_password
from django.views.decorators.csrf import csrf_exempt

# def index_view(request):
#     return render ( request , 'base.html' )

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        try:
            user = SimpleUser.objects.get(username=username)
            if check_password(password, user.password):  # Assuming you're using Django's check_password
                request.session['user_id'] = user.id  # Set user id in session
                return redirect('article_list')
        except SimpleUser.DoesNotExist:
            pass
    return render(request, 'app_cms/login.html')

@csrf_exempt
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
    if 'user_id' in request.session:
        del request.session['user_id']
    return redirect('login')

@csrf_exempt
def profile_view(request):
    user_id = request.session.get('user_id')
    if user_id:
        profile = SimpleUser.objects.get(id=user_id)
        context = {'profile': profile}
        return render(request, 'app_cms/profile.html', context)
    else:
        return redirect('login')

@csrf_exempt
def article_list(request):
    articles = Article.objects.all()
    context = {'articles': articles,}
    return render(request, 'app_cms/article_list.html', context)

@csrf_exempt
def article_detail(request, pk):
    article = Article.objects.get(pk=pk)
    context = {'article': article}
    return render(request, 'app_cms/article_detail.html', context)