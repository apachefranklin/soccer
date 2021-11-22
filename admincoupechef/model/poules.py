from django.db import models
from django.contrib import admin
from .team import Team
from .edition import Edition
from django.conf import settings


class Poule(models.Model):
    name=models.CharField(max_length=50)
    add_date=models.DateField(auto_now_add=True)
    edition=models.ForeignKey(Edition,on_delete=models.CASCADE,null=False)
    add_by=models.ForeignKey(settings.AUTH_USER_MODEL,null=False,on_delete=models.CASCADE)

    def __str__(self):
        return self.name+"("+self.edition.name+")"


class PouleTeam(models.Model):
    team=models.ForeignKey(Team,on_delete=models.CASCADE,null=False)
    poule=models.ForeignKey(Poule,on_delete=models.CASCADE,null=False)
    goals=models.SmallIntegerField(default=0)
    points=models.SmallIntegerField(default=0)
    conceded_goals=models.SmallIntegerField(default=0)
    goals_average=models.SmallIntegerField(default=0)
    add_by=models.ForeignKey(settings.AUTH_USER_MODEL,null=False,on_delete=models.CASCADE)

    def __str__(self):
        return self.team.name+" "+self.poule.__str__()


class PouleAdmin(admin.ModelAdmin):
    list_display=["id","name","edition","add_date","add_by"]
    search_fields=["id","name"]



class PouleTeamAdmin(admin.ModelAdmin):
    list_display=["id","team","poule","points","goals","conceded_goals","goals_average","add_by"]
    search_fields=["team","poule","goals_average"]
    list_filter=["team","poule"]