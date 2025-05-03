from django.shortcuts import render



def home_page(request):
    return render(request, 'jobia/home_page.html')

def dashboard(request):
    return render(request, 'jobia/dashboard.html')