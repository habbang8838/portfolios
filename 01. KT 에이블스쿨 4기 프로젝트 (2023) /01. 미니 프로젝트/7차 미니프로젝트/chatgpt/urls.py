# blog/urls.py
from django.urls import path
from . import views
from .views import chat

app_name = 'chatgpt'
urlpatterns = [
    path('', views.index, name='index'),
    path('chat', chat.as_view()),
]
