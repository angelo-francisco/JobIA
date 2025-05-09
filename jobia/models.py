from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class Curriculum(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=80, null=True, blank=True)
    form_data = models.JSONField(default=dict, null=True, blank=True)
    curriculum = models.FileField(upload_to="curriculums", null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True)
