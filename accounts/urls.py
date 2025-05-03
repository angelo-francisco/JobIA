from django.urls import path
from .views import login, logout, signup, check_username, check_email


urlpatterns = [
    path("check-username/<username>/", check_username, name="check_username"),
    path("check-email/<email>/", check_email, name="check_email"),
    path("login/", login, name="login"),
    path("signup/", signup, name="signup"),
    path("logout/", logout, name="logout"),
]
