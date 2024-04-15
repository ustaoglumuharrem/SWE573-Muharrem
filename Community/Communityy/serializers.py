
from rest_framework import serializers
from .models import Communityy

class CommunityySerializer(serializers.ModelSerializer):
    class Meta:
        model = Communityy
        fields = '__all__'



