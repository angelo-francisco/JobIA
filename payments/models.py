from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class Plan(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)
    limits = models.JSONField(default=dict)

    def __str__(self):
        return self.name
    
    def get_limit(self, feature, default=False):
        return self.limits.get(feature, default)


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
        return f"{self.user.username} - {self.plan.name}"

    def can_use_feature(self, feature):
        return (
            self.plan.get_limit(feature)
            if self.is_active else False
        )

    def get_remaining_usage(self, feature):
        if not self.can_use_feature(feature):
            return 0
        
        used = ResouceUsage.objects.filter(
            subscription=self,
            resource=feature
        ).count()

        total_allowed = self.can_use_feature(feature)
        return max(0, total_allowed - used)



class ResouceUsage(models.Model):
    subscription = models.ForeignKey(
        Subscription,
        on_delete=models.CASCADE,
    )
    resource = models.CharField(max_length=50, null=True, blank=True)
    amount_used = models.PositiveIntegerField(default=0)
