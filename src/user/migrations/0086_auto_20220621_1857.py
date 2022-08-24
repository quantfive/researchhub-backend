# Generated by Django 2.2 on 2022-06-21 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0085_auto_20220525_2043'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gatekeeper',
            name='type',
            field=models.CharField(choices=[('EDITOR_PAYOUT_ADMIN', 'EDITOR_PAYOUT_ADMIN'), ('ELN', 'ELN'), ('CLIENT_PERMISSIONS', 'CLIENT_PERMISSIONS'), ('PAYOUT_EXCLUSION', 'PAYOUT_EXCLUSION'), ('PERMISSIONS_DASH', 'PERMISSIONS_DASH')], db_index=True, max_length=128),
        ),
    ]