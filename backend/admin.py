from django.contrib import admin
from user import models
from course import models
from enrollment import models

class AppUserAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'email', 'username','first_name','last_name', 'is_staff', 'created_datetime','created_ip','last_ip', 'last_login', 'is_active', 'is_loggedin', 'profile_pic','access_token','session_id','google_id')
    search_fields = ('username', 'email', 'first_name', 'last_name')

admin.site.register(models.AppUser, AppUserAdmin)
admin.site.register(models.Category)
admin.site.register(models.Course)
admin.site.register(models.Enrollment)
admin.site.register(models.Role)