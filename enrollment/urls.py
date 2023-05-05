from . import views
from django.urls import path
from django.contrib import admin

urlpatterns = [
    path('enroll/<int:pk>/',views.EnrollmentView.as_view(), name='enroll-course'),
    path('usercourses/', views.CourseView.as_view(), name='course-list')
]
