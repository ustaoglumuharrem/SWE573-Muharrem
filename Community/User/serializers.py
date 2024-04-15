
from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class UserPasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['userName', 'password']

