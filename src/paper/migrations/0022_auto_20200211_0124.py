# Generated by Django 2.2.9 on 2020-02-11 01:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('paper', '0021_auto_20200121_0125'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='paper',
            options={'ordering': ['-paper_publish_date']},
        ),
    ]