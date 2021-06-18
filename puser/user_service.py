##Cette classe aura pour but de faire toutes les operations lies 
##au utilisateur et renvera toujours des reponses soit au formmat json \
##soit sous forme de dictionnaire mais le dictionnaire d'abord

from django.core.validators import validate_email
from django.contrib.auth.hashers import check_password
from django.urls import reverse
from django.shortcuts import redirect,render
from django.db.models import Q
import random
from .models import *
from pcontact.models import *

class UserService:
    def __init__(self,user=None):
        self.user=user
    
    def add(self,user,email=None,phone=None):
        response={"email_exist":False,
                  "phone_exist":False,
                  "valid_email":True,
                  "valid_phone":True,
                  "status":False,
                  "user":None,
                  "error":False}
        user.confirm_code=random.randint(10000,99999)
        if(email!=None):
            email_exist=Email.objects.filter(email__iexact=email.email)
            response["email_exist"]=len(email_exist)>0
        if(phone!=None):
            phone_exist=Phone.objects.filter(phone__iexact=phone.phone)
            response["phone_exist"]=len(phone_exist)>0
        if(response["phone_exist"]==False and response["email_exist"]==False):
            try:
                user.save()
                if(email!=None):
                    user.email_set.create(email=email.email,ip_address=user.ip_address)
                if(phone!=None):
                    user.phone_set.create(phone)
                response["user"]=user
                response["status"]=True
            except Exception as e:
                response["error"]=True
                response["emsg"]=str(e)

        return response
            #We add user
    @classmethod
    def get_user_role(cls,user):
        user_roles=UserRole.objects.filter(user=user).select_related("role")
        roles=[]
        for ur in user_roles:
            roles.append(ur.role.codename.lower())
        return roles
    

    def authenticate(self,email_phone,password):
        response={"status":False,"msg":"L'email n'existe pas, veuillez vous creez un compte ici"}
        success=False
        try:
            email=Email.objects.select_related("user").get(email__iexact=email_phone)
            password_db=email.user.password
            if(check_password(password,password_db)==True):
                success=True
            else:
                response["msg"]="Mot de passe incorrecte"
        except Exception as e:
            try:
                email=Phone.objects.select_related("user").get(phone__iexact=email_phone)
                password_db=phone.user.password
                if(check_password(password,password_db)==True):
                    success=True
                else:
                    response["msg"]="Mot de passe incorrecte"
            except:
                pass
        
        if success==True:
            response["status"]=True
            response["msg"]="Connexion effectuée avec success"
            response["email"]=email
            response["user"]={
                    "name":email.user.name,
                    "profil":email.user.profil,
                    "email":email.email,
                    "id":email.user.id,
                    "is_admin":email.user.is_admin,
                    "roles":UserService.get_user_role(Profile(id=email.user.id))
                }
            #On recuprere les roles de l'utilisateur

        return response    

    def is_authenticate(cls,request):
        """Cette fonction verifie si un utilisateur est authentifier ou pas"""
        authen=request.session.get("user",None)
        ##print(request.session)
        if(authen==None):
            redirect_ev=request.build_absolute_uri()
            to_redirect=redirect("login")
            to_redirect["location"]+="?redirect="+redirect_ev
            return to_redirect
        else:
            return True

    def activate_account(self,email,code):
        """Function who take code, and email like parameters
        ,verify if the two correspond to activate account"""

        response={"status":False,"msg":"Activation effectue avec succès"}

        email_o=Email(email=email)
        email_list=Email.objects.filter(~Q(user=None),email__iexact=email.strip())
        if(len(email_list)<=0):
            response["msg"]="L'email n'existe pas,veuillez vous creez un compte"
        else:
            code_db=email_list[0].user.confirm_code
            if(code_db==code):
                user=email_list[0].user
                user.confirm_code=0
                user.confirmed=1
                user.save()
                response["status"]=True
                response["msg"]="Compte activé avec success"
            else:
                response["msg"]="Le code ne correspond pas, veuillez saisir a nouveau"
        return  response
    
    