from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    @property
    def subscription(self):
        try:
            return (
                self.subscriptions.filter(is_active=True).select_related("plan").first()
            )
        except Exception:
            return None
    