from dataclasses import fields
from rest_framework import serializers
from django.contrib.auth import get_user_model
import django.contrib.auth.password_validation as validations
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from insta.models import Post
from insta.serializers.common import PostSerializer, NestUserSerializer, CommentSerializer
from ..models import DM
User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    
    password = serializers.CharField(write_only=True)
    password_confirmation = serializers.CharField(write_only=True)
    
    def validate(self, data):
        
        password = data.pop('password')
        password_confirmation = data.pop('password_confirmation')
        
        if password != password_confirmation:
            raise serializers.ValidationError({ 'password_confirmation': 'Passwords do not match' })
        
        try:
            validations.validate_password(password=password)
        except ValidationError as e:
            raise serializers.ValidationError({ 'password': e.messages })
        
        data['password'] = make_password(password)
        return data

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password_confirmation')
        
        
class NestedPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'post_image', 'caption', 'liked_by', 'comments')
        

class UserDMSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'profile_image')

class PopulatedDMSerializer(serializers.ModelSerializer):
    send = UserDMSerializer(read_only=True)
    recipient = UserDMSerializer()
    class Meta:
        model = DM
        fields = '__all__'
        
class DMSerializer(serializers.ModelSerializer):
    class Meta:
        model = DM
        fields = '__all__'
        
class ProfileSerializer(serializers.ModelSerializer):
    posts_created = NestedPostSerializer(many=True)
    message_created = PopulatedDMSerializer(many=True)
    message_got = PopulatedDMSerializer(many=True)
    followed_by = NestUserSerializer(many=True)
    follows = NestUserSerializer(many=True)
    
    class Meta:
        model = User
        fields = '__all__'
        

class ProfileEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'profile_image', 'bio')
    
     