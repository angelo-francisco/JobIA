from django.urls import path
from .views import home_page, dashboard, new_curriculum, typeform_webhook, generate_curriculum


urlpatterns = [
    path("", home_page, name="home_page"),
    path("dashboard/", dashboard, name="dashboard"),
    path("curriculum/new/", new_curriculum, name="new_curriculum"),
    path("curriculum/generate/", generate_curriculum, name="generate_curriculum"),
    path("curriculum/typeform-webhook/", typeform_webhook, name="typeform_webhook")
]
