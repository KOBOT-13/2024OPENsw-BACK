from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth.password_validation import validate_password

class CustomUserSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'birth_date']


    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError("Passwords do not match.")
        
        validate_password(data['password1'])
        
        return data

    def create(self, validated_data):
        if validated_data['password1'] != validated_data['password2']:
            raise serializers.ValidationError({"password": "Passwords do not match."})

        user = CustomUser(
            username=validated_data['username'],
            email=validated_data['email'],
            birth_date=validated_data['birth_date'],
        )
        user.set_password(validated_data['password1'])
        user.save()
        return user