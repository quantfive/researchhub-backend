# Generated by Django 4.2.16 on 2024-11-01 13:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("paper", "0142_merge_20241026_1915"),
    ]

    operations = [
        migrations.AlterField(
            model_name="paperversion",
            name="paper",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="version",
                to="paper.paper",
            ),
        ),
    ]
