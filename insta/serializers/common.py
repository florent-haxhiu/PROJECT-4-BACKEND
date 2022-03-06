from dataclasses import fields
from pyexpat import model
from rest_framework import serializers
from django.contrib.auth import get_user_model
from ..models import Post, Comment

User = get_user_model()

class NestUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'profile_image', 'followed_by')
        
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        
class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'

class NestPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'post_image', 'caption', 'liked_by', 'author', 'comments', 'created_at')