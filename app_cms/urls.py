from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('profile/<int:pk>/', views.profile_view, name='profile'),
    path('article_list/', views.article_list, name='article_list'),
    path('<int:pk>/', views.article_detail, name='article_detail'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
]