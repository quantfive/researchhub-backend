# Generated by Django 2.2 on 2021-06-17 21:27

import datetime
from datetime import timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('researchhub_document', '0017_auto_20210617_0354'),
    ]

    operations = [
        migrations.AddField(
            model_name='researchhubunifieddocument',
            name='published_date',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2021, 6, 17, 21, 27, 57, 929528, tzinfo=timezone.utc)),
            preserve_default=False,
        ),
    ]
