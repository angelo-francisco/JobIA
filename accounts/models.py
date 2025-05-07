from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    @property
    def actual_subscription_plan(self):
        try:
            return (
                self.subscriptions.filter(is_active=True).select_related("plan").first()
            )
        except Exception:
            return None
