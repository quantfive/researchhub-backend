# Generated by Django 2.2.5 on 2019-09-18 21:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0002_author_university'),
    ]

    operations = [
        migrations.CreateModel(
            name='Paper',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('authors', models.ManyToManyField(blank=True, related_name='authored_papers', to='user.Author')),
            ],
        ),
    ]
