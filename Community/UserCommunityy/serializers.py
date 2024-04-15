
from rest_framework import serializers
from .models import UserCommunityy

class UserCommunityySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCommunityy
        fields = '__all__'



