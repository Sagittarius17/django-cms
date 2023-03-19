from django.urls import path

from . import views

app1_urls = [    path('polls/', views.results, name='results'),]
app2_urls = [    path('details/', views.detail, name='detail'),]

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
]
