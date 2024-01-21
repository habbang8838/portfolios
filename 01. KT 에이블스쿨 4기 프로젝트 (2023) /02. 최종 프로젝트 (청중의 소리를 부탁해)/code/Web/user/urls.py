from django.urls import path

from . import views

app_name = "user"

urlpatterns = [
    path("signup/", views.signup_view, name="signup"),
    path('check_userid/', views.check_userid_existence, name='check_userid'),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
]
