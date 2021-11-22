from django.urls import path
from . import views

app_name="admincoupe"
urlpatterns = [
    path("",views.home_admin,name="home"),
    path("players",views.players,name="player"),
    path("poules",views.poules,name="poule"),
    path("editions",views.editions,name="edition")
]
