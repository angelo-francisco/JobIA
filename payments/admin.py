from django.contrib import admin
from .models import Plan, Subscription, ResouceUsage


admin.site.register([Plan, Subscription, ResouceUsage])
