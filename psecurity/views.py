from django.shortcuts import render

# Create your views here.

def view_403(request):
    context={}
    return render(request,"psecurity/403.html",context)