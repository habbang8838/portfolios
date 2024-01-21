# Create your views here.
import re

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from user.models import User


@csrf_exempt
def check_userid_existence(request):
    if request.method == "GET":
        userid = request.GET.get('userid')
        is_taken = User.objects.filter(userid=userid).exists()

        return JsonResponse({'is_taken': is_taken})


@csrf_exempt
def signup_view(request):
    if request.method == "GET":
        return render(request, "user/sign_up.html")

    if request.method == "POST":
        userid = request.POST.get("userid")
        password = request.POST.get("password")
        password_confirm = request.POST.get("password_confirm")
        name = request.POST.get("name")
        email = request.POST.get("email")

        error_message = validate_signup_data(userid, password, password_confirm, name, email)
        if error_message:
            return render(request, "user/sign_up.html", {"error": error_message})

        user = User(
            userid=userid,
            password=make_password(password),
            name=name,
            email=email
        )
        user.save()

        return redirect("user:login")


def validate_signup_data(userid, password, password_confirm, name, email):
    return (
            validate_userid(userid) or
            validate_password(password, userid, name, email) or
            validate_password_confirmation(password, password_confirm)
    )


def validate_userid(userid):
    if not userid or not re.match("^[a-zA-Z0-9]{6,15}$", userid):
        return "아이디는 6~15자리의 영문자와 숫자로 이루어져야 합니다."

    if User.objects.filter(userid=userid).exists():
        return "이미 존재하는 사용자 ID입니다."

    return None


def validate_password(password, userid, name, email):
    if not password or len(password) < 8:
        return "비밀번호는 최소 8자 이상이어야 합니다."

    patterns = ["[0-9]", "[a-z]", "[A-Z]", "[^0-9a-zA-Z]"]
    if sum(bool(re.search(pattern, password)) for pattern in patterns) < 3:
        return "비밀번호는 숫자, 소문자, 대문자, 특수 문자 중 최소 3가지를 포함해야 합니다."

    return None


def validate_password_confirmation(password, password_confirm):
    if password != password_confirm:
        return "비밀번호가 일치하지 않습니다."

    return None


@csrf_exempt
def login_view(request):
    if request.method == "GET":
        next_url = request.GET.get("next") or "/"
        return render(request, "user/login_page.html", {"next": next_url})

    if request.method == "POST":
        next_url = request.POST.get("next") or "/"
        userid = request.POST.get("userid").strip()
        password = request.POST.get("password").strip()
        remember_me = request.POST.get("remember_me")

        if not userid or not password:
            return render(request, "user/login_page.html", {"error": "아이디와 비밀번호를 입력해주세요.", "next": next_url})

        user = authenticate(request, username=userid, password=password)
        if user is not None:
            login(request, user)
            request.session.set_expiry(3600 * 24 * 30 if remember_me else 0)

            if next_url.startswith("/live/record/"):
                return redirect("live:info")
            else:
                return redirect(next_url)
        else:
            return render(request, "user/login_page.html", {"error": "아이디 또는 비밀번호가 올바르지 않습니다."})


@csrf_exempt
def logout_view(request):
    logout(request)
    return redirect("/")
