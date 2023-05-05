from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser,  PermissionsMixin

class AppUserManager(BaseUserManager):
     def create_user(self, email, username, password=None, first_name='', last_name='',profile_pic=''):
               if not email:
                    raise ValueError("Users must have an email address")
               if not username:
                    raise ValueError("Users must have a username")
               user = self.model(
                    email=self.normalize_email(email),
                    username=username,
                    first_name=first_name,
                    last_name=last_name,
                    profile_pic=profile_pic 
                    
               )
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
    role_id = models.IntegerField(default=3)
    created_datetime = models.DateTimeField(auto_now_add=True)
    created_ip = models.CharField(max_length=255,blank=True)
    last_login = models.DateTimeField(blank=True, null=True)
    last_ip = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)
    is_loggedin = models.BooleanField(default=False)
    profile_pic= models.URLField(max_length=255, blank=True)
#     profile_pic_image = models.ImageField(upload_to='profile_pics', blank=True)
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


class Role(models.Model):
    role_id = models.AutoField(primary_key=True)
    role_name = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.role_name
    
    class Meta:
        db_table = 'role'

class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.category_name

    class Meta:
        db_table = 'category'

# class Courses(models.Model):
#     course_id = models.AutoField(primary_key=True)
#     course_name = models.CharField(max_length=255, blank=True)
#     category_id = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
#     course_description = models.CharField(max_length=255, blank=True)
#     course_image = models.URLField(max_length=255, blank=True)

#     def __str__(self):
#         return self.course_name
    
#     class Meta:
#         db_table = 'course'


# class Course(models.Model):
#     category=models.ForeignKey(Category, on_delete=models.CASCADE)
#     teacher=models.ForeignKey(AppUser, on_delete=models.CASCADE,related_name='teacher_courses')
#     title=models.CharField(max_length=150)
#     description=models.TextField()
#     featured_img=models.ImageField(upload_to='course_img/',blank=True)
#     techs=models.TextField(blank=True)


#     def __str__(self):
#         return self.title

# from django.db import models

class Course(models.Model):
    name = models.CharField(max_length=100,blank=True)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    # user = models.ForeignKey(AppUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Enrollment(models.Model):
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    ROLE_CHOICES = [
        (1, 'admin'),
        (2, 'editor'),
        (3, 'viewer')
    ]
    role = models.IntegerField(choices=ROLE_CHOICES)