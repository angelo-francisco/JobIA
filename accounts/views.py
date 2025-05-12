from functools import wraps

import regex
from django.contrib import messages
from django.contrib.auth import (
    authenticate,
    get_user_model,
)
from django.contrib.auth import (
    login as django_login,
)
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_GET

User = get_user_model()


def just_not_authenticated_user(view):
    @wraps(view)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("home_page")
        return view(request, *args, **kwargs)

    return wrapper


@require_GET
def check_username(request, username):
    username = username.strip()

    if not username:
        return JsonResponse({"msg": "Preencha o campo, por favor."}, status=400)

    if User.objects.filter(username=username).exists():
        return JsonResponse({"msg": "Username indisponível."}, status=400)

    return JsonResponse({"msg": "Username disponível."})


@require_GET
def check_email(request, email):
    email = email.strip()

    if not email:
        return JsonResponse({"msg": "Preencha o campo, por favor."}, status=400)

    if User.objects.filter(email=email).exists():
        return JsonResponse({"msg": "Email já está sendo utilizado."}, status=400)

    return JsonResponse({"msg": "Email disponível."})


@just_not_authenticated_user
def login(request):
    if request.method == "POST":
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "").strip()
        remember = request.POST.get("remember") == "on"

        if not email or not password:
            messages.error(request, "Preencha todos os campos")
            return redirect("login")

        if remember:
            request.session.set_expiry((3600 * 24) * 14)
        else:
            request.session.set_expiry(0)

        user = authenticate(request, username=email, password=password)

        if user is not None:
            django_login(request, user)

            messages.success(request, "Autenticado com sucesso.")
            return redirect("dashboard")
        messages.error(request, "Email ou Palavra-passe incorrectos.")
        return redirect("login")
    return render(request, "auth/login.html")


@just_not_authenticated_user
def signup(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "").strip()

        if not username or not email or not password:
            messages.error(request, "Preencha todos os campos")
            return redirect("signup")

        if regex.search(r"[^a-zA-Z0-9]", username):
            messages.error(request, "O username só pode conter letras e números-")
            return redirect("signup")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Este username já está em uso.")
            return redirect("signup")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email já está em uso.")
            return redirect("signup")

        if not len(password) >= 8:
            messages.error(request, "Palavra-passe muito curta")
            return redirect("signup")

        User.objects.create_user(username=username, email=email, password=password)

        messages.success(request, "Novo usuário criado com sucesso.")
        return redirect("login")

    return render(request, "auth/signup.html")


def logout(request):
    return render(request, "auth/logout.html")
