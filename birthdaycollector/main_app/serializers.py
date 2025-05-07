from rest_framework import serializers
from .models import Birthday, Party
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta: 
        model = User
        fields = ('id', 'username', 'email')
        
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )

        return user
    
class PartySerializer(serializers.ModelSerializer):
    class Meta:
        model = Party
        fields = '__all__'

class BirthdaySerializer(serializers.ModelSerializer):
    parties = PartySerializer(many=True, read_only=True)
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    
    class Meta:
        model = Birthday
        fields = '__all__'
        
