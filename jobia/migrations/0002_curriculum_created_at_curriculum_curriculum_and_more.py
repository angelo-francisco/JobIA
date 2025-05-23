# Generated by Django 5.2 on 2025-05-09 20:56

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("jobia", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="curriculum",
            name="created_at",
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name="curriculum",
            name="curriculum",
            field=models.FileField(blank=True, null=True, upload_to="curriculums"),
        ),
        migrations.AddField(
            model_name="curriculum",
            name="form_data",
            field=models.JSONField(blank=True, default=dict, null=True),
        ),
        migrations.AddField(
            model_name="curriculum",
            name="user",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
