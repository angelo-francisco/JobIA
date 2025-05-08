from django.urls import path
from .views import upgrade_your_plan


urlpatterns = [
    path("upgrade/", upgrade_your_plan, name="upgrade_your_plan")
]
