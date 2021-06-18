from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.hashers import make_password
from .user_service import Profile, UserService, UserRole , Role
from base.utility import Utility

from pcontact.models import Phone, Email

import json

def perform_add_user(request):
    user_id=request.user.id
    user=Profile(pk=user_id)
    roles_list=Role.objects.filter(state=True)
    roles_dict={role.codename:role.id for role in roles_list}

    name=request.POST["user_name"].strip()
    last_name=request.POST["user_last_name"].strip()
    phone=request.POST["user_phone"].strip()
    email=request.POST["user_email"].strip()
    addresse=request.POST["user_address"].strip()
    sex=request.POST["user_sex"].strip()
    ip_address=request.META.get('REMOTE_ADDR')

    password_char=Utility.get_random_string(6)
    password=make_password(password_char,hasher="argon2")

    user_to_save=Profile(name=name,last_name=last_name,sex=sex,address=addresse,utype="admin",is_admin=True,password=password)
    user_to_save.ip_address=ip_address
    user_to_save.parent=user
    user_to_save.save()
    #on va recuperer les roles qui ont ete envoyes
    users_role=[]
    for key in roles_dict.keys():
        vale=request.POST.get(key,"").strip()
        if(vale!=""):
            role=Role(id=roles_dict[key])
            users_role.append(UserRole(user=user_to_save,role=role))
    Phone.objects.create(phone=phone,user=user_to_save)
    Email.objects.create(email=email,user=user_to_save,ip_address=ip_address)
    UserRole.objects.bulk_create(users_role)

    result={"status":True,"msg":"Utilisateur ajouté avec success"}
    
    return JsonResponse(result)
