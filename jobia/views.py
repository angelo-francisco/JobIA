from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache


def home_page(request):
    print(request.user.is_authenticated)
    return render(request, "jobia/home_page.html")


@login_required
@never_cache
def dashboard(request):
    return render(request, "jobia/dashboard.html")
