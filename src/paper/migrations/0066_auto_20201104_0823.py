# Generated by Django 2.2 on 2020-11-04 08:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('paper', '0065_vote_is_removed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vote',
            name='is_removed',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
