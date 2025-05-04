from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page
from django.views.decorators.cache import never_cache


@cache_page(60 * 15)
def home_page(request):
    return render(request, "jobia/home_page.html")


@login_required
@never_cache
def dashboard(request):
    return render(request, "jobia/dashboard.html")
