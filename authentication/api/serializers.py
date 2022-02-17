from asyncore import write
from dataclasses import fields
import email
from lib2to3.pgen2 import token
from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from authentication.models import User


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length = 68 ,min_length = 8, write_only = True )


    class Meta:
        model = User
        fields = ['email','username','password']
    

    def validate(self, attrs):
        email = attrs.get('email','')
        username = attrs.get('username','')

        if not username.isalnum():
            raise serializers.ValidationError('The username should be only contain alphanuemric  character')
        
        return attrs
    
    def create(self, validated_data):

        return User.objects.create_user(**validated_data)


class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length = 555)

    class Meta:
        model = User
        fields =['token'] 

class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length = 68 , min_length = 8 , write_only = True)
    username = serializers.CharField(read_only = True)
    tokens = serializers.CharField(read_only = True)
    class Meta:
        model = User
        fields = ['email','username','password','tokens']

    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')

        user =  authenticate(email = email, password = password)
        
        if not user:
            raise AuthenticationFailed('Invalid Credentials, Please Try Again')
        if not user.is_active:
            raise AuthenticationFailed("Account Is not Active Anymore, Please Contract With Admin")
        if not user.is_verified:
            raise AuthenticationFailed('Your account is not varified yet, Please check the email to verify')
        data = {
            'username': user.username,
            'email':user.user.email,
            'tokens': user.tokens
        
        }
        return data