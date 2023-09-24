from django.urls import path
from . import views

urlpatterns = [
    # path('', views.index_view, name='index'),
    path('', views.article_list, name='article_list'),
    path('<int:pk>/', views.article_detail, name='article_detail'),
    
    path('profile/', views.profile_view, name='profile'),
    path('update_profile/', views.UpdateProfileView.as_view(), name='update_profile'),
    
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
]