from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Profile,ProfileAdmin)
admin.site.register(Role,RoleAdmin)
admin.site.register(UserRole,UserRoleAdmin)