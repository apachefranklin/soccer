from django.urls import path, include
from . import views, api_form, admin_views,admin_views_api
from django.contrib.auth import views as auth_views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenVerifyView, TokenRefreshView

from rest_framework import routers
router=routers.DefaultRouter()
router.register(r"profiles/fdfas/",api_form.ProfileDetail)
urlpatterns = [
    #path configure and complte profile
    path("complete/setphone/",views.completephone,name="completephone"),
    path("complete/setphoneperform",api_form.setphonenumber,name="pcompletephone"),
    
    #path("login/",views.user_login,name="login"),
    path("api/profiles/",include(router.urls)),
    #password url
    path("password_change/",auth_views.PasswordChangeView.as_view(),name="password_change"),
    path("password_change/done/",auth_views.PasswordChangeDoneView.as_view(),name="password_change_done"),
    path("password_reset/",auth_views.PasswordResetView.as_view(),name="password_reset"),
    #registration and login url
    path('signup',views.user_signup,name='signup'),
    path("login/",views.user_login,name="login"),
    path("logout/",views.logout,name="logout"),
    path("signup/perform",api_form.signup_perform,name="psignup"),
    path("login/perform",api_form.login_perform,name="plogin"),
    #profil url
    path("edit",views.edit,name="edit_profil"),
    path("signup/confirm_email",views.confirm_email,name="confirmemail"),
    path("signup/confirm_email_perform",api_form.confirm_email_perform,name="performconfirmemail"),
    path("send-email-again/signup/<email>",views.send_registration_code_aigain,name="regiscodeagain"),
    path('new-password',views.request_password,name="new_password"),
    path("sdfosjfsvvdfp/user/admin/",admin_views.add_user,name="admin"),
    path("jfsdfsdkjsc/user/admin/padd",admin_views_api.perform_add_user,name="padd"),
    path("profile",views.user_profil,name="profil"),
    path("updateprofil",views.update_profil,name="updateprofil"),
    path("pupdateprofil",api_form.upadte_profil_perform,name="pupdateprofil"),
    path("changepasssword",views.change_password,name="changepwd"),
    path("pchangepassword",api_form.change_password_perform,name="pchangepwd"),
    path("change-profil-picture",views.change_profil_picture,name="changepicture"),
    path("change-profil-picture-perform",api_form.change_profil_picture_perform,name="pchangepicture"),
    path("send-email-pwd-reset",api_form.send_email_to_pwd_reset,name="pemailpwdreset"),
    path("confirm-code-sended",views.confirm_code_for_pwd_reset,name="pwdcodeconfirm"),
    path("perform-confirm-code-sended",api_form.perform_code_for_pwd_reset,name="ppwdcodeconfirm"),
    path("perform-password-reset",api_form.perform_reset_password,name="ppwdreset"),

    #api configuration path
    path("api/performlogin/",TokenObtainPairView.as_view(),name="performapilogin"),
    path("api/refreshlogin/",TokenRefreshView.as_view(),name="refreshtoken"),
    path("api/verifytoken/",TokenVerifyView.as_view(),name="verififytoken"),
    path("api/get_my_information/",api_form.get_my_information,name="getmyinformation")
]
