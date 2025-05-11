from django.urls import path
from .views import home_page, dashboard, new_curriculum, generate_curriculum, get_form_data


urlpatterns = [
    path("", home_page, name="home_page"),
    path("dashboard/", dashboard, name="dashboard"),
    path("curriculum/new/", new_curriculum, name="new_curriculum"),
    path("curriculum/generate/<slug>/", generate_curriculum, name="generate_curriculum"),
    path("curriculum/get-form-data/", get_form_data, name="get_form_data")
]
