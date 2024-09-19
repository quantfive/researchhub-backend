# Generated by Django 4.2.15 on 2024-09-19 22:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("paper", "0133_paperfetchlog_next_cursor"),
    ]

    operations = [
        migrations.AddField(
            model_name="paperfetchlog",
            name="server",
            field=models.CharField(
                blank=True,
                choices=[
                    ("biorxiv", "biorxiv"),
                    ("medrxiv", "medrxiv"),
                    ("arxiv", "arxiv"),
                    ("chemrxiv", "chemrxiv"),
                    ("preprints.org", "preprints.org"),
                ],
                max_length=255,
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="paperfetchlog",
            name="updated_date",
            field=models.DateTimeField(auto_now=True),
        ),
    ]
