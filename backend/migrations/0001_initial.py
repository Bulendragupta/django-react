# Generated by Django 3.2.18 on 2023-04-21 05:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='AppUser',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('user_id', models.AutoField(primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=50, unique=True)),
                ('username', models.CharField(max_length=50, unique=True)),
                ('first_name', models.CharField(blank=True, max_length=255)),
                ('last_name', models.CharField(blank=True, max_length=255)),
                ('is_staff', models.BooleanField(default=False)),
                ('created_datetime', models.DateTimeField(auto_now_add=True)),
                ('created_ip', models.CharField(blank=True, max_length=255)),
                ('last_login', models.DateTimeField(blank=True, null=True)),
                ('last_ip', models.CharField(blank=True, max_length=255)),
                ('is_active', models.BooleanField(default=True)),
                ('is_loggedin', models.BooleanField(default=False)),
                ('profile_pic_urls', models.URLField(blank=True, max_length=255)),
                ('profile_pic', models.ImageField(blank=True, upload_to='profile_pics')),
                ('access_token', models.CharField(blank=True, max_length=255)),
                ('session_id', models.CharField(blank=True, max_length=255)),
                ('google_id', models.CharField(blank=True, max_length=255)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'db_table': 'user_profile',
            },
        ),
    ]
