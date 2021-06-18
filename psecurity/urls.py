from django.urls import path
from . import views

app_name="psecurity"
urlpatterns = [
    path("not-authorise",views.view_403,name="403")
]
