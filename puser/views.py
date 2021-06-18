from django.shortcuts import render,redirect, loader, HttpResponse
from django.contrib.auth import authenticate,logout as dj_logout, login as dj_login
from django.contrib.auth.models import User
from django.utils.translation import gettext as _
from django.http import JsonResponse
from .models import Profile
from .forms import LoginForms, UserEditForm, ProfileEditForm, UserRegistrationForm
from psecurity.role_control import must_not_login,login_required_perso


# Create your views here.
@must_not_login
def user_login(request):
    form=LoginForms()
    request.session["redirect"]=request.GET.get("redirect","/")
    request.session.save()
    return render(request,"puser/login.html",{"form":form})
@must_not_login
def user_signup(request):
    form=UserRegistrationForm()
    form.email=request.GET.get("email","")
    request.session["redirect"]=request.GET.get("redirect","/")
    request.session.save()
    form.username="".join(request.GET.get("name","").split())
    context={"form":form}
    return render(request,"puser/signup.html",context)

@login_required_perso
def logout(request):
    dj_logout(request)
    context={"form":LoginForms()}
    #return render(request,"registration/login.html",context)
    return redirect("/")

@login_required_perso
def dashboard(request):
    return render(request,"account/dashboard.html")


@must_not_login 
def request_password(request):
    return render(request,"puser/password/request_new_password.html")
@must_not_login
def confirm_code_for_pwd_reset(request):
    return render(request,"puser/password/confirm_code_sended.html")

@must_not_login
def confirm_email(request):
    context={}
    return render(request,"registration/confirm_registration_code.html",context)

@login_required_perso
def user_profil(request):
    user_id=request.user.id
    user=User.objects.filter(id=user_id).select_related("profile").first()
    ##print("session on profil")
    ##print(request.session["user"])
    redirect_url=request.session.get("redirect",None)
    if(redirect_url!=None):
        request.session.pop("redirect")
        request.session.save()
        to_redirect=redirect(redirect_url)
        return to_redirect
    context={"user":user}
    return render(request,"puser/profil_user.html",context)

@login_required_perso
def change_password(request):
    context={}
    return render(request,"puser/change_password.html",context)

@login_required_perso
def update_profil(request):
    user_id=request.user.id
    user=User.objects.filter(id=user_id).select_related("profile").first()
    context={"user":user}
    return render(request,"puser/update_profil.html",context) 

@login_required_perso
def change_profil_picture(request):
    context={}
    return render(request,"puser/change_profil_picture.html",context)



@must_not_login
def send_registration_code_aigain(request,email):
    result={"status":False,"msg":"aucun compte n'est associé à cette adresse émail"}
    emails=Email.objects.filter(email=email)
    if(emails):
        user=emails[0].user
        code=str(user.confirm_code)
        email=emails[0].email
        name=user.name
        data={"sender_email":"noreply@protogons.com",
                      "receiver":[email], "sender_name":"Protogons", "subject":"Confirmation de l'addresse email",
                      "code":code,"email":email,"name":name }
        msg=loader.render_to_string("puser/email/activation_email.html",data)
        data["msg"]=msg
        EmailService.send_email("protogons",[email],data=data)
        result["status"]=True
        result["msg"]="émail renvoyé avec succès"
    
    return JsonResponse(result)

@login_required_perso
def edit(request):
    if request.method=="POST":
        user_form = UserEditForm(instance=request.user,data=request.POST)
        profile_form=ProfileEditForm(instance=request.user.profile,data=request.POST,files=request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
    else:
        user_form=UserEditForm(instance=request.user)
        profile_form=ProfileEditForm(instance=request.user.profile)
    
    return render(request,"puser/edit.html",{"user_form":user_form,"profile_form":profile_form})


#view for complete phone number
def completephone(request):
    data={"title":_("Numero de téléphone")}
    return render(request,"puser/completeprofil/phone_number.html",data)