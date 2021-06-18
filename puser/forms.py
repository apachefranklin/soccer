from django import forms
from django.utils.translation import gettext as _
from django.contrib.auth.models import User
from .models import Profile

class LoginForms(forms.Form):
    username=forms.CharField(label=_("nom d'utilisateur ou émail"),widget=forms.TextInput(attrs={"placeholder":_("émail ou nom d'utilisateur")}))
    password=forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
    password=forms.CharField(label=_("mot de passe"),widget=forms.PasswordInput)
    password2=forms.CharField(label=_("repetez le mot de passe"),widget=forms.PasswordInput)

    class Meta:
        model=User
        fields=('username','last_name',"email")
    
    def clean_password2(self):
        cd=self.cleaned_data
        if cd['password']!=cd['password2']:
            raise forms.ValidationError(_("les mots de passes ne sont pas identiques"))
        return cd["password2"]



class UserEditForm(forms.ModelForm):
    class Meta:
        model=User
        fields=("first_name","last_name","email")

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model=Profile
        fields=("birthdate","photo","profil","sex","address")


class PhotoUpdate(forms.ModelForm):
    photo=forms.ImageField(label=_("Photo de profil"))
    class Meta:
        model=Profile
        fields=("photo",)