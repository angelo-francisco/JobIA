from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("", include("jobia.urls")),
    path("admin/", admin.site.urls),
    path("auth/", include("accounts.urls")),
] 
