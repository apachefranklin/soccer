from django.db import models
from django.contrib import admin
from django.conf import settings

class Team(models.Model):
    name=models.CharField(max_length=50,null=False)
    abreviation=models.CharField(max_length=50,null=False,default="team")
    add_date=models.DateField(auto_now_add=True)
    logo=models.CharField(default="default.png",max_length=50)
    add_by=models.ForeignKey(settings.AUTH_USER_MODEL,null=False,on_delete=models.CASCADE)

    def __str__(self):
        return self.abreviation


class TeamAdmin(admin.ModelAdmin):
    list_display=["id","name","abreviation","add_date","logo","add_by"]
    list_filter=["add_by"]
    search_fields=["name","add_by"]