# Generated by Django 5.1.4 on 2025-04-21 16:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("reputation", "0099_alter_distribution_amount"),
    ]

    operations = [
        migrations.AddField(
            model_name="bountysolution",
            name="awarded_amount",
            field=models.DecimalField(
                decimal_places=10,
                default=0,
                help_text="Amount awarded to this solution",
                max_digits=19,
            ),
        ),
        migrations.AddField(
            model_name="bountysolution",
            name="status",
            field=models.CharField(
                choices=[
                    ("SUBMITTED", "SUBMITTED"),
                    ("AWARDED", "AWARDED"),
                    ("REJECTED", "REJECTED"),
                ],
                default="SUBMITTED",
                max_length=16,
            ),
        ),
    ]
