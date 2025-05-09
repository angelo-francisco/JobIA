import json

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt

from payments.decorators import user_has_feature_access


def home_page(request):
    print(request.user.is_authenticated)
    return render(request, "jobia/home_page.html")


@login_required
@never_cache
def dashboard(request):
    print(request.user.subscription.get_remaining_usage("max_curriculos"))
    return render(request, "jobia/dashboard.html")


@login_required
@user_has_feature_access("max_curriculos")
def new_curriculum(request):
    return render(request, "jobia/new_curriculum.html")


@login_required
@csrf_exempt
def typeform_webhook(request):
    if request.method == "POST":
        payload = json.loads(request.body)
        request.session["typeform-payload"] = payload
        return redirect("")
    return redirect("dashboard")


@login_required
def generate_curriculum(request): ...
