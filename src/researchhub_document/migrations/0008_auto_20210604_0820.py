# Generated by Django 2.2 on 2021-06-04 08:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hub', '0019_remove_hubmembership_created_at'),
        ('researchhub_document', '0007_auto_20210604_0739'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='researchhubunifieddocument',
            name='hubs',
        ),
        migrations.AddField(
            model_name='researchhubpost',
            name='hubs',
            field=models.ManyToManyField(blank=True, related_name='related_documents', to='hub.Hub'),
        ),
    ]