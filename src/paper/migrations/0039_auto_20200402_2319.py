# Generated by Django 2.2.11 on 2020-04-02 23:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('paper', '0038_merge_20200326_2341'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paper',
            name='doi',
            field=models.CharField(blank=True, default=None, max_length=255, null=True, unique=True),
        ),
    ]