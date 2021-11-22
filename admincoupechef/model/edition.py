from django.db import models
from django.contrib import admin
from django.conf import settings


# Create your models here.

class Edition(models.Model):
    name=models.CharField(max_length=50,null=False)
    begin_date=models.DateField(null=True,default=None)
    end_date=models.DateField(null=True,default=None)
    programmed=models.BooleanField(default=False)
    active=models.BooleanField(default=False)
    add_by=models.ForeignKey(settings.AUTH_USER_MODEL,null=False,on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class EditionAdmin(admin.ModelAdmin):
    list_display=["id","add_by","name","begin_date","end_date","programmed","active"]
