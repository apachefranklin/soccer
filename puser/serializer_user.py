from django.contrib.auth.models import User, Group
from .model.user import Profile
from rest_framework import serializers

class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model=Profile
        fields=["url","add_date","sex","address","profil"]

class UserSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = User
        fields = ['url', 'username', 'email',"first_name","last_name","is_active", 'groups',"profile"]
    profile=ProfileSerializer()