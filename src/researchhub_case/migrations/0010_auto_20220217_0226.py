# Generated by Django 2.2 on 2022-02-17 02:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('paper', '0082_auto_20210717_0708'),
        ('researchhub_case', '0009_auto_20220213_2241'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='authorclaimcase',
            name='context_content_id',
        ),
        migrations.RemoveField(
            model_name='authorclaimcase',
            name='context_content_type',
        ),
        migrations.AddField(
            model_name='authorclaimcase',
            name='target_paper',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='paper.Paper'),
        ),
        migrations.AlterField(
            model_name='authorclaimcase',
            name='case_type',
            field=models.CharField(choices=[('AUTHOR_CLAIM', 'AUTHOR_CLAIM'), ('PAPER_CLAIM', 'PAPER_CLAIM')], max_length=32),
        ),
    ]