from django.http import JsonResponse
from django.shortcuts import render,redirect


def login_required_perso(fonction):
    """Functiion who test if user is log befor call 
       a views in django views or order"""
    def p_mutable(*params,**named_params):
        request_test=params[0]
        url_to_redirect=request_test.build_absolute_uri()
        if(not request_test.user.is_authenticated):
            #We make a redirection by a sigin function
            redirect_response=redirect("login")
            redirect_response["location"]+="?redirect="+url_to_redirect
            return redirect_response
        
        return fonction(*params,**named_params)
    return p_mutable

def must_not_login(fonction):
    def p_mutable(*params,**named_params):
        request_test=params[0]
        if(request_test.user.is_authenticated):
            redirect_url=request_test.GET.get("redirect","/")
            redirect_response=redirect(redirect_url)
            return redirect_response
        else:
            return fonction(*params,**named_params)
    return p_mutable



def must_be_admin(fonction):
    @login_required_perso
    def p_mutable(*params,**named_params):
        request_p=params[0]
        is_admin=request_p.request.user.is_staf
        if(is_admin==False):
             redirect_response=redirect("psecurity:403")
             return redirect_response
        else:
             return fonction(*params,**named_params)
    return p_mutable


def have_role(role):
    def decorator(fonction):
        @login_required_perso
        def p_mutable(*params,**named_params):
          request_p=params[0]
          roles=request_p.session["user"]["roles"]
          if((role.lower() in roles) or "all_role" in roles):
              return fonction(*params,**named_params)
          else:
              return redirect("psecurity:403")
        return p_mutable
    return decorator 

