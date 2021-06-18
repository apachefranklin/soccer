from django.shortcuts import render

# Create your views here.

def home_admin(request):
    context={}
    return render(request,"admincoupechef/index.html",context)

def players(request):
    context={}
    return render(request,"admincoupechef/players.html",context)

def poules(request):
    context={}
    return render(request,"admincoupechef/poules.html",context)

def editions(request):
    context={}
    return render(request,"admincoupechef/editions.html",context)
