from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.hashers import make_password, check_password
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.views import View
import json
from django.core.files.storage import FileSystemStorage

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
        phn_num = request.POST['phn_num']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        
        if password == confirm_password:
            # IMPORTANT: Always hash the password before storing!
            hashed_password = make_password(password)
            
            user = SimpleUser(username=username, email=email, phn_num=phn_num, password=hashed_password)
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
        context = {
            'is_authenticated': request.user.is_authenticated,
            'profile': profile
            }
        return render(request, 'app_cms/profile.html', context)
    else:
        return redirect('login')
    
@method_decorator(csrf_exempt, name='dispatch')
class UpdateProfileView(View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            user_id = request.session.get('user_id')

            if not user_id:
                return JsonResponse({'status': 'error', 'message': 'Not authenticated'}, status=401)

            user = SimpleUser.objects.get(pk=user_id)

            # Update the fields
            user.username = data.get('username', user.username)
            user.email = data.get('email', user.email)
            user.phn_num = data.get('phn_num', user.phn_num)
            
            # ... update any other fields you want ...

            user.save()
            return JsonResponse({'status': 'success', 'message': 'Profile updated successfully'})
        
        except SimpleUser.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'User not found'}, status=404)
        
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f"Error: {str(e)}"}, status=500)
        
def upload_profile_picture(request):
    if request.method == 'POST' and request.FILES['profile_pic']:
        profile_pic = request.FILES['profile_pic']
        user_id = request.session.get('user_id')
        print(user_id)
        
        # Fetch the user instance using the user_id
        user = SimpleUser.objects.get(pk=user_id)

        # Save the uploaded image
        fs = FileSystemStorage(location='static/images/')
        filename = fs.save(profile_pic.name, profile_pic)
        uploaded_file_url = fs.url(filename)

        # Update the user's profile picture
        user.profile_pic = uploaded_file_url
        user.save()

        return redirect('profile') 

    # return to profile page with some error message if needed
    return redirect('profile')

def new_article(request):
    user_id = request.session.get('user_id')
    profile = SimpleUser.objects.get(id=user_id)
    context = {
        'is_authenticated': request.user.is_authenticated,
        'profile': profile
        }
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        image = request.FILES['image']
        author = request.POST['author']
        if author == '':
            author = profile.username
        
        # Save the uploaded image
        fs = FileSystemStorage(location='static/images/')
        filename = fs.save(image.name, image)
        uploaded_file_url = fs.url(filename)

        # Save the article
        article = Article(title=title, content=content, image=uploaded_file_url, author=author)
        article.save()
        return redirect('article_list')

    
    return render(request, 'app_cms/new_article.html', context)

@csrf_exempt
def article_list(request):
    # articles = Article.objects.all()
    articles = Article.objects.all().order_by('-published_date') # '-' indicates descending order
    user_id = request.session.get('user_id')
    try:
        profile = SimpleUser.objects.get(id=user_id)
    except SimpleUser.DoesNotExist:
        profile = None
        return render(request, 'app_cms/article_list.html')
    context = {
        'is_authenticated': request.user.is_authenticated,
        'articles': articles, 'profile': profile
        }
    return render(request, 'app_cms/article_list.html', context)

@csrf_exempt
def article_detail(request, pk):
    article = Article.objects.get(pk=pk)
    user_id = request.session.get('user_id')
    profile = SimpleUser.objects.get(id=user_id)
    context = {
        'is_authenticated': request.user.is_authenticated,
        'article': article, 'profile': profile
        }
    return render(request, 'app_cms/article_detail.html', context)