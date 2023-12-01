from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.hashers import make_password, check_password
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views import View
import json
from django.core.files.storage import FileSystemStorage
from .utils import get_user_profile
from django.contrib import messages
from django.utils.crypto import get_random_string
from datetime import datetime
from pathlib import Path


# def index_view(request):
#     return render ( request , 'base.html' )

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        try:
            user = SimpleUser.objects.get(username=username)
            if check_password(password, user.password):  # using Django's check_password
                request.session['user_id'] = user.id  # Set user id in session
                messages.success(request, 'Successfully logged in!')
                return redirect('article_list')
            else:
                messages.error(request, 'Invalid username or password.')
        except SimpleUser.DoesNotExist:
            messages.error(request, 'Invalid username or password.')
            
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
    is_authenticated = bool(user_id)
    profile = get_user_profile(user_id)
    
    if profile:
        context = {
            'is_authenticated': is_authenticated,
            'profile': profile, 'user_id': user_id
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

        # Generate a unique filename based on the current timestamp and a random string
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        random_string = get_random_string(length=6)
        new_filename = f"profile_{user_id}_{timestamp}_{random_string}{Path(profile_pic.name).suffix}"

        # Save the uploaded image with the new filename
        fs = FileSystemStorage(location='static/images')
        filename = fs.save(new_filename, profile_pic)
        uploaded_file_url = fs.url(filename)

        # Update the user's profile picture
        user.profile_pic = uploaded_file_url
        user.save()

        return redirect('profile') 

    # return to profile page with some error message if needed
    return redirect('profile')


def new_article(request):
    user_id = request.session.get('user_id')
    is_authenticated = bool(user_id)
    profile = SimpleUser.objects.get(id=user_id)
    context = {
        'is_authenticated': is_authenticated,
        'profile': profile, 'user_id': user_id
        }
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        image = request.FILES['image']
        author = request.POST['author']
        if author == '':
            author = profile.username
        
        # Generate a unique filename based on the current timestamp and a random string
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        random_string = get_random_string(length=6)
        new_filename = f"{author}_{timestamp}_{random_string}{Path(image.name).suffix}"

        # Save the uploaded image with the new filename
        fs = FileSystemStorage(location='static/images/')
        filename = fs.save(new_filename, image)
        uploaded_file_url = fs.url(filename)

        # Save the article
        article = Article(title=title, content=content, image=uploaded_file_url, author=author)
        article.save()
        return redirect('article_list')

    return render(request, 'app_cms/new_article.html', context)


@csrf_exempt
def article_list(request):
    articles = Article.objects.all().order_by('-published_date') # '-' indicates descending order
    user_id = request.session.get('user_id')
    is_authenticated = bool(user_id)
    print(is_authenticated)
    
    # Increment view count only if the user is authenticated
    if user_id and Article.objects.filter(id=user_id).exists():
        article = Article.objects.get(id=user_id)
        article.view_count += 1
        article.save()
    
    try:
        profile = SimpleUser.objects.get(id=user_id)
    except SimpleUser.DoesNotExist:
        profile = None
        # return render(request, 'app_cms/article_list.html')
    context = {
        'is_authenticated': is_authenticated,
        'articles': articles, 'profile': profile, 'user_id': user_id
        }
    return render(request, 'app_cms/article_list.html', context)


def edit_article(request, pk):
    article = Article.objects.get(pk=pk)
    user_id = request.session.get('user_id')
    is_authenticated = bool(user_id)
    
    try:
        profile = SimpleUser.objects.get(id=user_id)
    except (KeyError, SimpleUser.DoesNotExist):
        return redirect('login')  # or wherever you want to redirect them to.
    
    if request.method == 'POST':
        # Get the new details from POST data
        title = request.POST['title']
        content = request.POST['content']
        author = profile.username
        print(author)
        
        
        # If an image is uploaded, handle it
        if 'image' in request.FILES:
            image = request.FILES['image']
            
            # Generate a unique filename based on the current timestamp and a random string
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            random_string = get_random_string(length=6)
            new_filename = f"{author}_{timestamp}_{random_string}{Path(image.name).suffix}"
            
            fs = FileSystemStorage(location='static/images/')
            filename = fs.save(new_filename, image)
            uploaded_file_url = fs.url(filename)
            article.image = uploaded_file_url

        # Update article details
        article.title = title
        article.content = content
        # Update other fields as required

        # Save the changes
        article.save()

        # Redirect to the list or detail view after saving changes
        return redirect('article_detail', pk=article.pk)
    context = {
        'is_authenticated': is_authenticated,
        'article': article, 'profile': profile, 'user_id': user_id
        }

    return render(request, 'app_cms/edit_article.html', context)


def delete_article(request, pk):
    article = Article.objects.get(pk=pk)
    article.delete()
    return redirect('article_list')


@csrf_exempt
def article_detail(request, pk):
    article = Article.objects.get(pk=pk)
    article.increment_view_count()
    user_id = request.session.get('user_id')
    is_authenticated = bool(user_id)
    
    if user_id:
        profile = SimpleUser.objects.get(id=user_id)
    else:
        profile = None

    context = {
        'is_authenticated': is_authenticated,
        'article': article, 'profile': profile, 'user_id': user_id
        }
    return render(request, 'app_cms/article_detail.html', context)
