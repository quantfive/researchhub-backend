# Generated by Django 4.2.13 on 2024-07-12 14:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0118_rename_merged_with_author_id_author_merged_with_author"),
    ]

    operations = [
        migrations.CreateModel(
            name="UserVerification",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("first_name", models.TextField()),
                ("last_name", models.TextField()),
                (
                    "status",
                    models.TextField(
                        choices=[
                            ("APPROVED", "Approved"),
                            ("DECLINED", "Declined"),
                            ("PENDING", "Pending"),
                        ]
                    ),
                ),
                (
                    "verified_by",
                    models.TextField(
                        choices=[("MANUAL", "Manual"), ("PERSONA", "Persona")]
                    ),
                ),
                ("external_id", models.TextField()),
                ("created_date", models.DateTimeField(auto_now_add=True)),
                ("updated_date", models.DateTimeField(auto_now=True)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]