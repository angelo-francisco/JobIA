from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", include("jobia.urls")),
    path("admin/", admin.site.urls),
    path("auth/", include("accounts.urls")),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
