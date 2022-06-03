# Generated by Django 2.2 on 2022-05-14 00:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0081_verdict'),
    ]

    operations = [
        migrations.AlterField(
            model_name='verdict',
            name='verdict_choice',
            field=models.CharField(choices=[('ABUSIVE_OR_RUDE', 'ABUSIVE_OR_RUDE'), ('COPYRIGHT', 'COPYRIGHT'), ('LOW_QUALITY', 'LOW_QUALITY'), ('NOT_CONSTRUCTIVE', 'NOT_CONSTRUCTIVE'), ('PLAGIARISM', 'PLAGIARISM'), ('SPAM', 'SPAM'), ('NOT_ABUSIVE_OR_RUDE', 'NOT_ABUSIVE_OR_RUDE'), ('NOT_COPYRIGHT', 'NOT_COPYRIGHT'), ('NOT_LOW_QUALITY', 'NOT_LOW_QUALITY'), ('NOT_NOT_CONSTRUCTIVE', 'NOT_NOT_CONSTRUCTIVE'), ('NOT_PLAGIARISM', 'NOT_PLAGIARISM'), ('NOT_SPAM', 'NOT_SPAM')], max_length=32),
        ),
    ]