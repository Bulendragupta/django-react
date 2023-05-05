from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser,  PermissionsMixin

class AppUserManager(BaseUserManager):
     # def create_user(self, email, username, password=None):
     #      if not email:
     #           raise ValueError("Users must have an email address")
     #      if not username:
     #           raise ValueError("Users must have a username")
     #      user = self.model(
     #           email=self.normalize_email(email),
     #           username=username
     #      )
     #      user.set_password(password)
     #      user.save(using=self._db)
     #      return user

     # def create_user(self, email, username, password=None, first_name='', last_name='',profile_pic=''):
     #      if not email:
     #           raise ValueError("Users must have an email address")
     #      if not username:
     #           raise ValueError("Users must have a username")
     #      user = self.model(
     #           email=self.normalize_email(email),
     #           username=username,
     #           first_name=first_name,
     #           last_name=last_name,
     #           profile_pic=profile_pic 
               
     #      )
     #      user.set_password(password)
     #      user.save(using=self._db)
     #      return user

     def create_user(self, email, username, password=None, first_name='', last_name='', profile_pic=''):
          if not email:
               raise ValueError("Users must have an email address")
          if not username:
               raise ValueError("Users must have a username")
          
          user = self.model(
               email=self.normalize_email(email),
               username=username,
               first_name=first_name,
               last_name=last_name,
          )
          
          if profile_pic.startswith('http') or profile_pic.startswith('https'):
               user.profile_pic_url = profile_pic
          else:
               user.profile_pic = profile_pic
          
          user.set_password(password)
          user.save(using=self._db)
          return user


     def create_superuser(self, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class AppUser(AbstractBaseUser, PermissionsMixin):
    user_id = models.AutoField (primary_key=True)
    email = models.EmailField (max_length=50,unique=True)
    username = models.CharField(max_length=50,unique=True)
    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    role_id = models.IntegerField(blank=True)
    created_datetime = models.DateTimeField(auto_now_add=True)
    created_ip = models.CharField(max_length=255,blank=True)
    last_login = models.DateTimeField(blank=True, null=True)
    last_ip = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)
    is_loggedin = models.BooleanField(default=False)
    profile_pic_urls = models.URLField(max_length=255, blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics', blank=True)
    access_token = models.CharField(max_length=255, blank=True)
    session_id = models.CharField(max_length=255, blank=True)
    google_id = models.CharField(max_length=255, blank=True)

    USERNAME_FIELD= 'email'
    REQUIRED_FIELDS =[ 'username']
    objects = AppUserManager()
    
    def __str__(self):
        return self.username
    
    class Meta:
        db_table = 'user_profile'
