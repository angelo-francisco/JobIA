from functools import wraps
from django.shortcuts import redirect
from django.urls import reverse


def user_has_feature_access(feature):
    def decorator(view):
        @wraps(view)
        def wrapper(request, *args, **kwargs):
            subscription = request.user.subscription
            feature_value = subscription.plan.get_limit(feature)

            if isinstance(feature_value, (int, float)):
                remaining_usage = subscription.get_remaining_usage(feature)

                if remaining_usage <= 0:
                    return redirect(reverse("dashboard") + "?upgrade_plan=1")
            elif isinstance(feature_value, bool) and not subscription.can_use_feature(
                feature
            ):
                return redirect(reverse("dashboard") + "?upgrade_plan=1")

            return view(request, *args, **kwargs)

        return wrapper

    return decorator
