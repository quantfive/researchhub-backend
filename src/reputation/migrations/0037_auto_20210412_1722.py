# Generated by Django 2.2 on 2021-04-12 17:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reputation', '0036_auto_20210104_2043'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contribution',
            name='contribution_type',
            field=models.CharField(choices=[('AUTHOR', 'AUTHOR'), ('SUBMITTER', 'SUBMITTER'), ('UPVOTER', 'UPVOTER'), ('CURATOR', 'CURATOR'), ('COMMENTER', 'COMMENTER'), ('SUPPORTER', 'SUPPORTER'), ('VIEWER', 'VIEWER')], max_length=16),
        ),
    ]