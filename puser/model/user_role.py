from django.db import models
from django.contrib import admin
from .user import *
from .role import *

class UserRole(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    role=models.ForeignKey(Role,on_delete=models.CASCADE)
    add_date=models.DateTimeField(auto_now=True)

class UserRoleAdmin(admin.ModelAdmin):
    list_display=['user','role','add_date']
    search_fields=['user','role','add_date']