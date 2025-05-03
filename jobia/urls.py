from django.urls import path
from .views import home_page, dashboard


urlpatterns = [
    path("", home_page, name="home_page"),
    path("dashboard/", dashboard, name="dashboard")
]
