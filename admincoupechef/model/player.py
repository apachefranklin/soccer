from django.db import models
from django.contrib import admin
from django.conf import settings
from .edition import Edition
from .team import Team

class Player(models.Model):
    name=models.CharField(max_length=50,null=False)
    surname=models.CharField(max_length=50,null=True)
    matricule=models.CharField(max_length=20,null=True,default="00000")
    add_date=models.DateField(auto_now_add=True)
    add_by=models.ForeignKey(settings.AUTH_USER_MODEL,null=False,on_delete=models.CASCADE)

    def __str__(self):
        return self.name+"("+self.surname+")("+self.matricule+")"

class PlayerAdmin(admin.ModelAdmin):
    list_display=["id","name","surname","add_date","add_by"]
