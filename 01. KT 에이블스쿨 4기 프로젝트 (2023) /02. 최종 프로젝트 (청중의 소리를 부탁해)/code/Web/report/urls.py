from django.urls import path

from . import views

app_name = 'report'

urlpatterns = [
    path("list/", views.list_lectures, name="list_lectures"),
    path("result/<int:id>/", views.result, name="detail"),
    path("list/delete/", views.delete_lecture, name="delete_lecture"),
]
