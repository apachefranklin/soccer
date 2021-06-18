from .models import *


class ContactService:
    def __init__(self,email=None,phone=None):
        self.email=email
        self.phone=phone
    
    def add_email(self,email):
        response={"status":False,"email":None,"error":False}
        email_exist=Email.objects.filter(email=email.email)
        if(len(email_exist)==0):
            try:
                email=email.save()
                response["email"]=email
            except:
                response["error"]=True
        return response
    
    def add_phone(self,phone):
        response={"status":False,"phone":None,"error":False}
        phone_exist=Email.objects.filter(phone__ie=phone.phone)
        if(len(phone_exist)==0):
            try:
                phone=phone.save()
                response["phone"]=phone
            except:
                response["error"]=True
        return response       