from rest_framework import serializers
from jwt_auth.models import User
from .common import NestPostSerializer, NestUserSerializer, CommentSerializer, PostSerializer


class PopulatedUserSerializer(serializers.ModelSerializer):
    posts_created = NestPostSerializer(many=True)
    class Meta:
        model = User
        fields = '__all__' 
        
class PopulatedCommentSerializer(CommentSerializer):
    author = NestUserSerializer()
    
class PopulatedPostSerializer(PostSerializer):
    comments = PopulatedCommentSerializer(many=True, read_only=True)
    liked_by = NestUserSerializer(many=True, read_only=True)
    author = PopulatedUserSerializer()
    