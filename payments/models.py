from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Plan(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)
    limits = models.JSONField(default=dict)

    def __str__(self):
        return self.name


class Subscription(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="subscriptions"
    )
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    raw_data = models.JSONField(default=dict, null=True, blank=True)

    def __str__(self):
        return f"{self.user.user} - {self.plan.name}"


class ResouceUsage(models.Model):
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE, )
    resource = models.CharField(max_length=50, null=True, blank=True)
    amount_used = models.PositiveIntegerField(default=0)
