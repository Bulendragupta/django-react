# Generated by Django 3.2.18 on 2023-05-04 06:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0002_auto_20230421_1218'),
    ]

    operations = [
        migrations.AddField(
            model_name='appuser',
            name='role_id',
            field=models.IntegerField(blank=True, default=3),
        ),
    ]
