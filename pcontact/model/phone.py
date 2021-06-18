from django.db import models
from django.contrib import admin
from puser.models import *
class Phone(models.Model):
    phone=models.CharField(max_length=23)
    country_code=models.CharField(max_length=8)
    add_date=models.DateTimeField(auto_now=True)
    state=models.BooleanField(default=True)
    user=models.ForeignKey(settings.AUTH_USER_MODEL,null=True,blank=True,on_delete=models.SET_NULL)

class PhoneAdmin(admin.ModelAdmin):
    list_display=['phone','country_code','add_date','state']
    search_fields=['phone','country_code','state','add_date']