
from rest_framework import serializers
from .models import CommunityTemplate

class CommunityTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommunityTemplate
        fields = '__all__'



