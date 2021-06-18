from django.db import models
from django.contrib import admin
from puser.models import *
class Email(models.Model):
    email=models.CharField(max_length=200)
    state=models.BooleanField(default=True)
    add_date=models.DateTimeField(auto_now=True)
    ip_address=models.CharField(max_length=200, null=True)
    #user=models.ForeignKey(settings.AUTH_USER_MODEL,null=True,blank=True,on_delete=models.SET_NULL)

class EmailAdmin(admin.ModelAdmin):
    list_display=['id','email','state','add_date']
    list_filter=['state']
    search_fields=['email','state','add_date']