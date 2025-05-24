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
    get_interview_message,
    get_interview_messages,
    delete_interview
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
    path("interview/del/<slug>/", delete_interview, name="delete_interview"),
    path("interview/simulation/<slug>/", interview_simulation, name="interview_simulation"),
    path("interview/get-interview-message/<slug>/", get_interview_message, name="get_interviw_message"),
    path("interview/get-interview-messages/<slug>/", get_interview_messages, name="get_interview_messages"),
]
