from . import views
from django.urls import path
from django.contrib import admin


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
	path('register', views.UserRegister.as_view(), name='register'),
	path('login', views.UserLogin.as_view(), name='login'),
	path('logout', views.UserLogout.as_view(), name='logout'),
	path('user', views.UserView.as_view(), name='user'),
    path('user_profile/', views.user_profile.as_view(), name='user_profile'),
    
	
	path('category/',views.CategoryCreateView.as_view(), name='categorycreate'),
	path('course', views.CourseView.as_view(), name='category'),
    path('enroll-course/<int:pk>/',views.EnrollmentView.as_view(), name='enroll-course'),
    path('category/<int:pk>', views.CourseView.as_view(), name='category'),
    path('usercourses/', views.CourseView.as_view(), name='course-list'),
]