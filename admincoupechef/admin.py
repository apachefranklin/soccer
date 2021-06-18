from django.contrib import admin
from .models import *
# Register your models here.

from .models import *

admin.site.register(Team,TeamAdmin)
admin.site.register(Goal,GoalAdmin)
admin.site.register(Edition,EditionAdmin)
admin.site.register(Poule,PouleAdmin)
admin.site.register(PouleTeam,PouleTeamAdmin)
admin.site.register(Match,MatchAdmin)
admin.site.register(Player,PlayerAdmin)