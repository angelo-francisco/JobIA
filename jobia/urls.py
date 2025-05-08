from django.urls import path
from .views import home_page, dashboard, new_curriculum


urlpatterns = [
    path("", home_page, name="home_page"),
    path("dashboard/", dashboard, name="dashboard"),
    path("curriculum/new/", new_curriculum, name="new_curriculum")
]
