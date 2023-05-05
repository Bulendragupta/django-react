from django.db import models
from course.models import *
from user.models import *

class Enrollment(models.Model):
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    role = models.ForeignKey(Role,on_delete=models.CASCADE)
