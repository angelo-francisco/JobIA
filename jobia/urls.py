from django.urls import path
from .views import (
    home_page,
    dashboard,
    new_curriculum,
    generate_curriculum,
    get_form_data,
    delete_curriculum,
    interview_start,
    interview_simulation,
    get_interviw_message
)


urlpatterns = [
    path("", home_page, name="home_page"),
    path("dashboard/", dashboard, name="dashboard"),
    path("curriculum/new/", new_curriculum, name="new_curriculum"),
    path(
        "curriculum/generate/<slug>/", generate_curriculum, name="generate_curriculum"
    ),
    path("curriculum/get-form-data/", get_form_data, name="get_form_data"),
    path("curriculum/del/<slug>/", delete_curriculum, name="delete_curriculum"),
    path("interview/start/", interview_start, name="interview_start"),
    path("interview/simulation/<slug>/", interview_simulation, name="interview_simulation"),
    path("interview/get-interview-message/<slug>/", get_interviw_message, name="get_interviw_message"),
]
