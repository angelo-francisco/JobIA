from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    @property
    def subscription(self):
        return self.subscriptions.filter(is_active=True)
