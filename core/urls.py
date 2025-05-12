from django.contrib import admin
from django.urls import path, include
from django.conf import settings


urlpatterns = [
    path("", include("jobia.urls")),
    path("admin/", admin.site.urls),
    path("auth/", include("accounts.urls")),
    path("payments/", include("payments.urls")),
]

if settings.DEBUG:
    from debug_toolbar.toolbar import debug_toolbar_urls

    urlpatterns += debug_toolbar_urls(prefix="debug")
