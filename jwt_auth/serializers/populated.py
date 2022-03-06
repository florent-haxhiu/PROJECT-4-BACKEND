from rest_framework import serializers
from insta.serializers.common import NestUserSerializer
from .common import UserDMSerializer, ProfileSerializer, PostSerializer, CommentSerializer
from ..models import DM, User

        
class PopulatedCommentSerializer(CommentSerializer):
    author = NestUserSerializer()
        

class PopulatedPostSerializer(PostSerializer):
    comments = PopulatedCommentSerializer(many=True, read_only=True)
    liked_by = NestUserSerializer(many=True, read_only=True)
    author = ProfileSerializer()


class NestPopulatedUserSerializer(ProfileSerializer):
    following = NestUserSerializer(many=True)
    
class PopulatedUserSerializer(serializers.ModelSerializer):
    posts_created = PopulatedPostSerializer(many=True)
    following = NestUserSerializer(many=True, read_only=True)
    author = ProfileSerializer()
    class Meta:
        model = User
        fields = '__all__'
    