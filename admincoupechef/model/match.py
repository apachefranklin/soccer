from django.db import models
from django.contrib import admin
from django.conf import settings
from .team import Team
from .player import Player
from .edition import Edition


class GoalType(models.TextChoices):
    CSC="CSC"
    SP="SP"
    N="N"

class MatchType(models.TextChoices):
    FINAL="FINAL"
    SEMIFINAL="SEMIFINAL"
    POULE="POULE"
    AMICAL="AMICAL"

class MatchState(models.TextChoices):
    reported="reporte"
    current="en cours"
    cancel="annulé"
    finish="terminé"
    to_program="a programmé"
    

class Match(models.Model):
    add_date=models.DateField(auto_now_add=True)
    date_to_play=models.DateField(null=True)
    state=models.CharField(choices=MatchState.choices,default=MatchState.to_program,max_length=50)
    match_type=models.CharField(choices=MatchType.choices,default=MatchType.POULE,max_length=50)
    team1=models.ForeignKey(Team,on_delete=models.CASCADE,related_name="team1")
    team2=models.ForeignKey(Team,on_delete=models.CASCADE,related_name="team2")
    goal_team1=models.SmallIntegerField(default=0)
    goal_team2=models.SmallIntegerField(default=0)
    winner=models.SmallIntegerField(default=0)
    edition=models.ForeignKey(Edition,null=False,on_delete=models.CASCADE)
    add_by=models.ForeignKey(settings.AUTH_USER_MODEL,null=False,on_delete=models.CASCADE)
    title=models.CharField(max_length=50,default=None,null=True)

    def __str__(self):
        return self.team1.name+" vs "+self.team2.name+"("+self.edition.name+")"+"("+self.state+")"

class Goal(models.Model):
    player=models.ForeignKey(Player,on_delete=models.CASCADE,null=False)
    match=models.ForeignKey(Match,on_delete=models.CASCADE,null=False)
    goal_type=models.CharField(choices=GoalType.choices,max_length=50)
    add_by=models.ForeignKey(settings.AUTH_USER_MODEL,null=False,on_delete=models.CASCADE)


class MatchAdmin(admin.ModelAdmin):
    list_display=["id","team1","team2","date_to_play","goal_team1","goal_team2","edition","add_by"]

class GoalAdmin(admin.ModelAdmin):
    list_display=["id","player","match","goal_type","add_by"]



