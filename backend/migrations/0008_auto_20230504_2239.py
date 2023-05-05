# Generated by Django 3.2.18 on 2023-05-04 17:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0007_alter_category_category_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='featured_img',
        ),
        migrations.RemoveField(
            model_name='course',
            name='teacher',
        ),
        migrations.RemoveField(
            model_name='course',
            name='techs',
        ),
        migrations.RemoveField(
            model_name='course',
            name='title',
        ),
        migrations.AddField(
            model_name='course',
            name='name',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.DeleteModel(
            name='Courses',
        ),
    ]
