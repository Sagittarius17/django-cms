from django.urls import path

from . import views

app_name = "app_polls"
urlpatterns = [
    path("", views.polls, name="polls"),
    path('new/poll/', views.new_poll, name='new_poll'),
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    path("<int:pk>/results/", views.ResultsView.as_view(), name="results"),
    path("<int:question_id>/vote/", views.vote, name="vote"),
]