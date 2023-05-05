from . import views
from django.urls import path
from django.contrib import admin

urlpatterns = [
    path('category/',views.CategoryCreateView.as_view(), name='categorycreate'),
    #course creation update delete 
    path('course', views.CourseView.as_view(), name='category'),
    #course enrollment
    path('category/<int:pk>', views.CourseView.as_view(), name='category')
]