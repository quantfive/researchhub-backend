# Generated by Django 4.2.15 on 2024-09-09 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("paper", "0132_paper_authorship_authors"),
    ]

    operations = [
        migrations.AddField(
            model_name="paperfetchlog",
            name="next_cursor",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]