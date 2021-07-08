# Generated by Django 2.2 on 2021-06-11 22:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('researchhub_document', '0013_auto_20210604_1925'),
        ('discussion', '0036_auto_20210415_2112'),
    ]

    operations = [
        migrations.AddField(
            model_name='thread',
            name='post',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='threads', to='researchhub_document.ResearchhubPost'),
        ),
    ]