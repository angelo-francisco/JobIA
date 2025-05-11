import json

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from payments.decorators import user_has_feature_access


def home_page(request):
    return render(request, "jobia/home_page.html")


@login_required
@never_cache
def dashboard(request):
    return render(request, "jobia/dashboard.html")


@login_required
@user_has_feature_access("max_curriculos")
def new_curriculum(request):
    return render(request, "jobia/new_curriculum.html")


@login_required
@user_has_feature_access("max_curriculos")
def get_form_data(request): ...


@login_required
@user_has_feature_access("max_curriculos")

def generate_curriculum(request):
    return render(request, 'jobia/generate_curriculum.html')
