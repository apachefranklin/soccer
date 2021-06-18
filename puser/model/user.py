from django.db import models
from django.contrib import admin
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save


class Profile(models.Model):
    user=models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="profile")
    SEX=(('M',"MASCULIN"),("F","FEMININ"),("I","INDETERMINATE"))
    #USERNAME_FIELD='username'
    #EMAIL_FIELD='email'
    status = models.BooleanField(default=False)
    add_date = models.DateTimeField(auto_now_add=True)
    sex=models.CharField(max_length=1,default="I",choices=SEX)
    birthdate=models.DateField(null=True,blank=True)
    confirm_code=models.CharField(max_length=8,default="0000")
    renitialisation_code=models.CharField(max_length=200,default="0000")
    address=models.CharField(max_length=200,null=True)
    utype=models.CharField(max_length=30,default="user",null=True)
    confirmed=models.BooleanField(default=False)
    profil=models.CharField(max_length=200,default="default.png")
    photo=models.ImageField(upload_to="puser/profils/%Y/%m/%d/",blank=True)
    pseudo=models.CharField(max_length=200,null=True,blank=True)
    is_admin=models.BooleanField(default=False)
    parent=models.ForeignKey("self",null=True,on_delete=models.SET_NULL,blank=True)
    ip_address=models.GenericIPAddressField(default='19.3.202.3')
    phone_number=models.PositiveIntegerField(default=0,null=False)
    baned=models.BooleanField(default=False,help_text="allow us to know if used where baned nor not")

    def find_all_email(self):
        return self.email_set.all()
    
    def find_all_phone(self):
        return self.phone_set.all()
    
    def __str__(self):
        return f'Profile for user { self.user.username }'

class ProfileAdmin(admin.ModelAdmin):
    list_display=['id',"user","photo","profil","parent","sex","birthdate"]
    search_fields=['id','first_name','last_name']


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()