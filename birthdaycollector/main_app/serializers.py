from rest_framework import serializers
from .models import Birthday, Party

class PartySerializer(serializers.ModelSerializer):
    class Meta:
        model = Party
        fields = '__all__'

class BirthdaySerializer(serializers.ModelSerializer):
    parties = PartySerializer(many=True, read_only=True)
    
    class Meta:
        model = Birthday
        fields = '__all__'
        
