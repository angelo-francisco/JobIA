from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from payments.models import Plan, Subscription

User = get_user_model()


@receiver(post_save, sender=User)
def create_user_subscription(sender, instance, created, **kwargs):
    if created:
        plan = Plan.objects.get(name="Essencial")
        Subscription.objects.create(
            user=instance,
            plan=plan,
        )
