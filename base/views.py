from django.shortcuts import render
from django.db.models import Count
from admincoupechef.models import PouleTeam, Team, Edition,Player,Match,MatchState,Goal,GoalType

# Create your views here.

def home(request):
    active_edition=Edition.objects.filter(active=True)
    poules=[]
    classements=[]
    goals=Goal.objects.exclude(goal_type=GoalType.CSC).values("player").annotate(nbgoal=Count("id"),nbmatch=Count("match")).order_by("-nbgoal","match")
    for i,elt in enumerate(goals):
        goals[i]["player"]=Player.objects.filter(id=goals[i]["player"]).first()
    print("Goals is goal",goals)
    if(len(active_edition)>0):
        active_edition=active_edition[0]
        poules=active_edition.poule_set.all()
        poule_name=[elt.name for elt  in poules]
        #maintenant nous devons reuperr le classement de chaque poule
        classements={}
        for poule in poules:
            classement=PouleTeam.objects.filter(poule=poule).order_by("-points","-goals_average")
            classements[poule.name]=classement
    players=Player.objects.all()[:10]
    teams=Team.objects.all()

    next_match=Match.objects.filter(state=MatchState.to_program).order_by("date_to_play","id").first()
    #next_match=matchs.first()

    match_not_play=Match.objects.exclude(state=MatchState.finish)
    played_match=Match.objects.filter(state=MatchState.finish).order_by("-date_to_play","-id")
    all_match=Match.objects.all().order_by("date_to_play","id")

    context={"active_edition":active_edition,"poules":poules,"standing":classements,"players":players,"teams":teams,"matchs":all_match,"next_match":next_match,"not_played":match_not_play,"played":played_match,"goals":goals}
    return render(request,"basecoupechef/index.html",context)

def calender(request):
    match_not_play=Match.objects.exclude(state=MatchState.finish).order_by("date_to_play")
    played_match=Match.objects.filter(state=MatchState.finish).order_by("-date_to_play")
    all_match=Match.objects.all().order_by("date_to_play")
    context={"to_plays":match_not_play,"played_matchs":played_match,"all_match":match_not_play}
    return render(request,"basecoupechef/calendrier.html",context)
