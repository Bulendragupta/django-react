from django.urls import path,include
from django.contrib import admin


urlpatterns = [
    #user register and login
    path('admin/', admin.site.urls,name='myadmin'),
	path('', include('user.urls'),name="user"),
    path('', include('course.urls'),name="course"),
    path('', include('enrollment.urls'),name="enrollment")

]