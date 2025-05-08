from django.shortcuts import render


def upgrade_your_plan(request):
    return render(request, "payments/upgrade.html")