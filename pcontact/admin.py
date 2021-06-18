from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Phone,PhoneAdmin)
admin.site.register(Email,EmailAdmin)