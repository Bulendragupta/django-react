from django.db import models

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
    course_id= models.IntegerField(primary_key=True)
    course_name = models.CharField(max_length=100,blank=True)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    course_img = models.ImageField(upload_to='course_img/',blank=True)

    def __str__(self):
        return self.name