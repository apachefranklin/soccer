from django.shortcuts import render
from .user_service import Profile, UserService, UserRole , Role
from psecurity.role_control import have_role

@have_role("user_add")
def add_user(request):
    roles=Role.objects.filter(state=True).order_by("name")
    user_list=Profile.objects.all()
    context={"roles":roles,"user_list":user_list}
    return render(request,"puser/admin/user_home.html",context)