# Generated by Django 2.2.12 on 2020-04-29 20:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('paper', '0046_auto_20200429_0102'),
    ]

    operations = [
        migrations.AddField(
            model_name='paper',
            name='vote_avg_epoch',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='paper',
            name='discussion_count',
            field=models.IntegerField(db_index=True, default=0),
        ),
        migrations.AlterField(
            model_name='paper',
            name='score',
            field=models.IntegerField(db_index=True, default=0),
        ),
    ]