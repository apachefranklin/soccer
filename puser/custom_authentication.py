from django.contrib.auth.models import User



class EmailAuthBackend(object):
     def authenticate(self,request=None,username=None,password=None):
         try:
             user=User.objects.filter(email=username).select_related("profile").first()
             if user is not None:
                if user.check_password(password):
                    return user
             return None
         except User.DoesNotExist:
             return None
    
     def get_user(self,user_id):
         try:
             user=User.objects.filter(pk=user_id).select_related("profile").first()
             return user
         except User.DoesNotExist:
             return None

class MyModelAuthBackend(object):
    def authenticate(self,request=None,username=None,password=None):
         try:
             user=User.objects.filter(username=username).select_related("profile").first()
             if user is not None:
                if user.check_password(password):
                    return user
             return None
         except User.DoesNotExist:
             return None
    
    def get_user(self,user_id):
        try:
            user=User.objects.filter(pk=user_id).select_related("profile").first()
            return user
        except User.DoesNotExist:
            return None

