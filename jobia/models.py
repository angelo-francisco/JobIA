from django.db import models
from django.conf import settings
from cloudinary.models import CloudinaryField
from shortuuid import uuid
from uuid import uuid4

User = settings.AUTH_USER_MODEL


class StatusChoices(models.TextChoices):
    COMPLETE = "C", "Complete"
    INCOMPLETE = "I", "Incomplete"


class Curriculum(models.Model):
    """
    Model Curriculum

    Contains all the data related to the generated curriculums
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(
        "Title", max_length=80, null=True, blank=True, default="(Sem Nome)"
    )
    status = models.CharField(
        "Status",
        max_length=10,
        null=True,
        blank=True,
        choices=StatusChoices,
        default=StatusChoices.INCOMPLETE,
    )
    form_data = models.JSONField("Form Raw Data", default=dict, null=True, blank=True)
    curriculum = CloudinaryField("Curriculum", null=True, blank=True)
    created_at = models.DateTimeField("Creation Date", auto_now=True)
    slug = models.SlugField("Slug", null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            generated_uuid = uuid()

            while Curriculum.objects.filter(slug__iexact=generated_uuid).exists():
                generated_uuid = uuid()

            self.slug = generated_uuid
        return super().save(*args, **kwargs)


class Interview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    role = models.CharField(max_length=50, null=True, blank=True)
    level = models.CharField(max_length=30, null=True, blank=True)
    status = models.CharField(
        "Status",
        max_length=10,
        null=True,
        blank=True,
        choices=StatusChoices,
        default=StatusChoices.INCOMPLETE,
    )
    started_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    slug = models.SlugField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = uuid4()

            while Interview.objects.filter(slug=base_slug).exists():
                base_slug = uuid4()

            self.slug = base_slug
        return super().save(*args, **kwargs)


class InterviewMessage(models.Model):
    interview = models.ForeignKey(Interview, on_delete=models.CASCADE, related_name="messages")
    sender = models.CharField(max_length=20, choices=[('U', 'User'), ('I', 'IA')])
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender} - {self.created_at.strftime('%H:%M:%S')}"