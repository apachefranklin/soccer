from django.db import models
from django.contrib import admin

class Role(models.Model):
    codename=models.CharField(max_length=100)
    name=models.CharField(max_length=200)
    state=models.BooleanField(default=True)
    add_date=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class RoleAdmin(admin.ModelAdmin):
    list_display=['id','name','codename','state','add_date']
    search_fields=['name','codename','state']