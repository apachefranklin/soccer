#ce fichier contiendra toutes 
#les fonctions de request de formulaires destiner
#aux utilisateurs
import re
import random
from django.http import HttpResponse,JsonResponse
from django.shortcuts import redirect
from django.core.validators import validate_email
from django.contrib.auth.hashers import make_password,check_password
from django.contrib.auth import authenticate,login
from django.contrib.auth.models import User
from .user_service import UserService
from .model.user import Profile
from pcontact.model.email import Email
from pcontact.model.phone import Phone
from pcontact.email_service import EmailService
from django.shortcuts import loader, redirect, reverse
from django.shortcuts import render
from base.utility import Utility
from base.file_service import FileService
from django.utils.translation import gettext as _
from psecurity.role_control import must_not_login
from .forms import LoginForms
from django.db.models import Q
from django.conf import settings
from .serializer_user import UserSerializer, ProfileSerializer
from rest_framework import viewsets
from rest_framework import permissions, authentication
from rest_framework_simplejwt import authentication as jwt_auth
from rest_framework.decorators import api_view, permission_classes, authentication_classes

import random
regex_phone=re.compile(r"^(\+\d{3}\d{9,})|(\d{9,})$")

auth_classes=authentication_classes([authentication.SessionAuthentication,jwt_auth.JWTAuthentication,jwt_auth.JWTTokenUserAuthentication])
@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def signup_perform_2(request):
    """Fonction qui permet d'enregistrer un nouvel utilisateur"""    
    response={"status":False}
    try:
        name=request.POST["name"].strip()
        email_phone=request.POST["email_phone"].strip()
        password=request.POST["pwd"]
        password2=request.POST["pwd2"]
        ip_address=request.META.get('REMOTE_ADDR')
        #We control the email field
        try:
            validate_email(email_phone)
        except:
            response["msg"]="Veuillez entrez une addresse email correcte"
            return JsonResponse(response)
        if(password!=password2):
            response["msg"]="Mot de passe non identique"
        else:
          
            user=Profile(ip_address=ip_address)
            if(uadd["status"]==True):
                confirm_email_location=redirect("confirmemail")
                response["redirect"]=confirm_email_location["location"]+"?redirect="+request.GET.get("redirect",None)+"&email="+email_phone
                response["status"]=True
                response["msg"]="Compte creer avec succes, veuillez confirmez votre addresse email,(Verifiez vos spam aussi)"
                #debut de la configuration de l'envoie du mail
                #print("before print")
                code=str(uadd["user"].confirm_code)
                data_mail={"sender_email":"noreply@protogons.com","receiver":[email_phone], "sender_name":"Protogons", "subject":"Confirmation de l'addresse email",
                      "code":code,"email":email_phone,"name":name }
                #print(uadd)
                msg=loader.render_to_string("puser/email/activation_email.html",data_mail)
                data_mail["msg"]=msg
                #print("bonjour ici les inscriptions emails")
                email_service=EmailService()
                EmailService.send_email("protogons",[email_phone],data=data_mail)
            elif(uadd["email_exist"]==True):
                response["msg"]="Cette addresse email n'est plus disponible"
            elif(uadd["phone_exist"]==True):
                response["msg"]="Ce numero de telephone n'est plus disponible"
            elif(uadd["error"]==True):
                response["msg"]="Une erreur innatendue s'est produite"
                response["emsg"]=uadd["emsg"]
    except Exception as e:
        response["execept"]=str(e)
        pass

@api_view(["POST"])
@must_not_login
def login_perform(request):
    """permet d'authentifier un utilisateur en utilisant son username qui peut etre
        soit son email, son numero de telphone soit son nom d'utilisateur et son mot de passe
        @param username
        @param password
    """
    form=LoginForms(request.POST)
    redirect_url=request.GET.get("redirect","")
    response={"status":False,"tags":"error","msg":"veuillez remplir correctement le formualaire"}
    if form.is_valid():
        cd=form.cleaned_data
        username=cd["username"].strip()
        password=cd["password"]
        user=authenticate(request=request,username=username,password=password)

        if user is not None:
            response["status"]=True
            response["tags"]="success"
            response["msg"]=_("connexion éffectuée avec succèss")
            response["user"]={"id":user.id,"username":user.username,"email":user.email,"first_name":user.first_name,"last_name":user.last_name,"phone_number":user.profile.phone_number}
            response["redirect"]=redirect_url
            login(request,user)

        else:
            response["msg"]=_("veuillez verfier votre mot de passe votre idenfiant. ils sont sensible à la case")
    return JsonResponse(response)

@must_not_login
@api_view(["POST"])
def signup_perform(request):
    """Fonction qui permet d'enregistrer un nouvel utilisateur"""    
    response={"status":False}
    try:
        username=request.POST["username"].strip()
        email_phone=request.POST["email"].strip()
        password=request.POST["password"]
        password2=request.POST["password2"]
        ip_address=request.META.get('REMOTE_ADDR')
        #We control the email field
        try:
            validate_email(email_phone)
        except:
            response["msg"]="Veuillez entrez une addresse email correcte"
            return JsonResponse(response)
        if(password!=password2):
            response["msg"]="Mot de passe non identique"
        else:
            user=User(username=username,email=email_phone)
            user.set_password(password)
            user_exist=User.objects.filter(Q(username=username)|Q(email=email_phone)).first()
            if(user_exist!=None):
                if(user_exist.username==username):
                    response["msg"]=_("ce nom d'utilisateur n'est plus disponible")
                else:
                    response["msg"]=_("addresse émail insdisponible")
            else:
                user.save()
                user.profile.confirm_code=random.randint(10000,99999)
                user.save()
                #on log une fois cet utilisateur
                user=authenticate(request,username=username,password=password)
                login(request,user)
                #utilisateur loggger
                confirm_email_location=redirect("home")
                response["redirect"]=confirm_email_location["location"]+"?redirect="+request.GET.get("redirect",None)+"&email="+email_phone

                response["status"]=True
                response["msg"]="Compte creer avec succes, veuillez confirmez votre addresse email,(Verifiez vos spam aussi)"
                #debut de la configuration de l'envoie du mail
                #print("before print")
                code=str(user.profile.confirm_code)
                
                data_mail={"sender_email":"noreply@protogons.com","receiver":[email_phone], "sender_name":"Protogons", "subject":"Confirmation de l'addresse email",
                      "code":code,"email":email_phone,"name":username }
                #print(uadd)
                msg=loader.render_to_string("puser/email/activation_email.html",data_mail)
                data_mail["msg"]=msg
                print(data_mail)
                #print("bonjour ici les inscriptions emails")
                #email_service=EmailService()
                #EmailService.send_email("protogons",[email_phone],data=data_mail)
    except Exception as e:
        
        pass
    return JsonResponse(response)

#definition of function to verify code associate to specifiec email
@api_view(["GET"])
def confirm_email_perform(request):
    code=request.GET.get("code",None)
    email=request.GET.get("email",None)
    from_url=request.GET.get("fromurl",None)
    #print(from_url)
    data=UserService().activate_account(email,code)
    if(data["status"]==True):
        url_to_redirect=str(request.GET.get("redirect","")).strip()
        if(url_to_redirect==""):
            url_to_redirect=redirect("pwb:home")["location"]
        data["redirect"]=url_to_redirect
        if(from_url):
            return redirect(url_to_redirect)
    return JsonResponse(data)


#This function define the first step to renitialise password
@api_view(["POST"])
def send_email_to_pwd_reset(request):
    context = {"title":"code_reinitialize","reset":"Reinitialise your password"}
    email=request.POST["email"].strip()
    emails=Email.objects.filter(email=email).select_related("user")
    result={"status":True,"msg":"Un email vous ete envoye avec success","redirect":""}
    if(len(emails)==1):
        email=emails[0]
        user=email.user
        context={"code":random.randint(10000,99999),"name":user.name,"email":email.email}
        user.renitialisation_code=context["code"]
        user.save()
        data={"msg":loader.render_to_string("puser/email/email_password_reset.html",context),"subject":"Renitialisation de mot de passe"}
        data["sender_email"]="noreply@protogons.com"
        EmailService.send_email("Protogons",[email.email],data)

        request.session["mail_reset"]=email.email
        request.session["user_reset"]=email.user.id

        return JsonResponse(result)
    else:
        result["status"]=False
        result["msg"]="Aucune n'addresse email n'est associer a ce compte. Veuillez vous en creer un"
        return JsonResponse(result)


#send email to perform verification of the code
@api_view(["POST"])
def perform_code_for_pwd_reset(request):
    email_s=request.GET.get("email","")
    code_s=request.GET.get("code","")
    email=Email.objects.filter(email__iexact=email_s).select_related("user")
    context={}
    result={"status":True,"msg":"Le code est correcte. Vous allez entrez votre nouveau mot de passe"}
    if(len(email)==1):
        email=email[0]
        user=email.user
        if(user.renitialisation_code==code_s and user.renitialisation_code!=0):
            #c'est cette variable qui va fair authoriser le changement de mot de passe
            request.session["mail_reset"]=email.email
            request.session["user_reset"]=user.id
            request.session["pwd_reset_auth"]=True
            return render(request,"puser/password/enter_new_password.html",context)

        else:
            context["msg"]="Le code que vous avez entré est incorrecte"
            return render(request,"puser/password/confirm_code_sended.html",context)  
    else:
        return render(request,"puser/password/failed_process.html",context)

@api_view(["POST"])
def perform_reset_password(request):
    password=request.POST["password1"]
    password2=request.POST["password2"]

    result={"status":True,"msg":"Mot de passe renitialisé avec succès"}
    if(password==password2):
        user_id=request.session["user_reset"]
        user=Profile.objects.get(id=user_id)
        user.password=make_password(password)
        user.renitialisation_code=0
        user.save()
        result["redirect"]=redirect("login")["location"]
    else:
        result["status"]=False
        result["msg"]="les deux mots de passe ne sont pas identique"
    return JsonResponse(result)


#Fonction pour modifier le profil d'un utilisateur
@api_view(["POST"])
@auth_classes
@permission_classes([permissions.IsAuthenticated])
def upadte_profil_perform(request):
    user_id=request.user.id
    user=User.objects.get(id=user_id)
    name=request.POST["name"].strip()
    last_name=request.POST["last_name"].strip()
    addresse=request.POST["address"].strip()
    sex=request.POST["sex"].strip().upper()
    user.last_name=name
    user.profile.address=addresse
    user.first_name=last_name
    user.profile.sex=sex
    user.save()
    request.user.last_name=name
    request.user.first_name=last_name

    result={"status":True,"msg":"Profil mise a jour avec succès"}

    result["redirect"]=redirect("profil")["location"]
    return JsonResponse(result)


#cette fonction permet a un utilisateur de renitialiser son mot de passe
@api_view(["POST"])
def change_password_perform(request):
    """ Cette fonction permet de modifier le mot de passe
    de l'utilisateut courant"""
    user_id=request.user.id
    user=Profile.objects.get(id=user_id)
    result={}
    password=request.POST["password"] 
    result["status"]=False
    result["msg"]="Vos mots de passe ne corresponde pas"
    if(check_password(password,user.password)):
        new_password=request.POST["new_password"]
        new_password_c=request.POST["new_password_c"]
        if(new_password_c==new_password):
            user.password=make_password(new_password,"argon2")
            user.save()
            result["status"]=True
            result["msg"]="Mot de passe mise a jour avec succès"
    else:
        result["msg"]="Mot de passe incorrecte"
    
    return JsonResponse(result)

@auth_classes
@permission_classes([permissions.IsAuthenticated])
def change_profil_picture_perform(request):
    user_id=request.user.id
    user=User.objects.get(id=user_id)
    img_profil=request.FILES["profil_picture"]
    extension=FileService.get_extension(img_profil.name)
    img_name=Utility.get_random_string()+"-"+str(random.randint(0,10000))
    img_name="".join(random.sample(img_name,len(img_name)))+"."+extension
    
    base_path="sharedapp/puser/static/puser/profils/"
    if settings.DEBUG==False:
        base_path=settings.STATIC_ROOT+"puser/profils/"
    file_path_save=base_path+img_name
    success_upload=FileService.move_upload(img_profil,file_path_save)
    if(success_upload==True):
        FileService.remove_file(base_path+user.profile.profil)
    user.profile.profil=img_name
    user.save()
    request.user.profile.profil=img_name
    ##print(request.session["user"])
    ##request.session["user"]["profil"]=img_name
    request.session.save()
    result={"status":True,"msg":"Photo de profil mise à jour avec succès"}

    context={"user":user}
    redirect_url=redirect("profil")
    return redirect_url


##Api permettant de recupeere les informations sur un utilisateur

@api_view(["POST"])
@auth_classes
@permission_classes([permissions.IsAuthenticated])
def get_my_information(request):
    user=request.user

    user =User.objects.get(id=user.id)
    serial_object=UserSerializer(user,context={"request":request})

    return JsonResponse(serial_object.data)    

@api_view(["POST"])
@auth_classes
@authentication_classes([permissions.IsAuthenticated])
def setphonenumber(request):
    #print(request.POST.keys())
    phone=(request.POST.get("phone_number","")).strip()
    result={"status":False,"msg":_("Numero de telephone incorrect")}
    if(regex_phone.match(phone)==None):
        return JsonResponse(result)
    else:
        user=request.user
        profil=user.profile
        profil.phone_number=phone
        profil.save()
        result["status"]=True
        result["msg"]="Téléphone enregistré avec succèss"
        result["redirect"]=request.POST.get("redirect",redirect("pwb:home")["location"])
        return JsonResponse(result)
    return JsonResponse(result)

class ProfileDetail(viewsets.ModelViewSet):
    queryset=Profile.objects.all()
    serializer_class=ProfileSerializer
    permission_classes=[permissions.IsAuthenticated]



