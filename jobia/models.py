from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class Curriculum(models.Model):
    """
    Model Curriculum

    Contains all the data related to the generated curriculums
    """

    class StatusChoices(models.TextChoices):
        COMPLETE = 'C', 'Complete'
        INCOMPLETE = 'I', 'Incomplete'

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField('Title', max_length=80, null=True, blank=True)
    status = models.CharField('Status', max_length=10, null=True, blank=True, choices=StatusChoices, default=StatusChoices.INCOMPLETE)
    form_data = models.JSONField('Form Raw Data', default=dict, null=True, blank=True)
    curriculum = models.FileField('Curriculum', upload_to="curriculums", null=True, blank=True)
    created_at = models.DateTimeField('Creatio Date', auto_now=True)
    slug = models.SlugField("Slug", null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            
        return super().save(*args, **kwargs)
