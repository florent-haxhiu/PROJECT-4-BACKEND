from django.db import IntegrityError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from .models import Post, Comment
from .serializers.common import PostSerializer, CommentSerializer
from .serializers.populated import PopulatedPostSerializer


class PostListView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, _request):
        posts = Post.objects.all()
        serial = PopulatedPostSerializer(posts, many=True)
        return Response(serial.data, status=status.HTTP_200_OK)

    def post(self, request):
        serialized_data = PostSerializer(data=request.data)
        print(request.data)
        try:
            print(serialized_data)
            serialized_data.is_valid()
            serialized_data.save()
            return Response(serialized_data.data, status=status.HTTP_201_CREATED)
        except IntegrityError as e:
            print(e)
            return Response({"detail": str(e)}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        except AssertionError as e:
            print(e)
            return Response({"detail": str(e)}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        except:
            return Response(
                {"detail": "Unprocessable Entity"},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )


class PostDetailView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Post.objects.all()
    serializer_class = PopulatedPostSerializer


class PostLikeView(APIView):
    permission_classes = (IsAuthenticated,)

    def get_post(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise NotFound(detail="Post not found")

    def post(self, request, post_pk):
        post = self.get_post(pk=post_pk)
        if request.user in post.liked_by.all():
            post.liked_by.remove(request.data.id)
        else:
            post.liked_by.add(request.data.id)
        serial = PostSerializer(post)
        return Response(serial.data, status=status.HTTP_201_CREATED)


class CommentListView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, pk):
        request.data['post'] = pk
        request.data['author'] = request.data.id
        created_comment = CommentSerializer(data=request.data)
        try:
            created_comment.is_valid()
            created_comment.save()
            return Response(created_comment.data, status=status.HTTP_201_CREATED)
        except:
            return Response(created_comment.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class CommentDetailView(APIView):
    permission_classes = (IsAuthenticated,)
    
    def get_comment(self, pk):
        try:
            return Comment.objects.get(pk=pk)
        except Comment.DoesNotExist:
            raise NotFound(detail="Comment not found")
    
    def delete(self, _request, comment_pk):
        comment_delete = self.get_comment(pk=comment_pk)
        comment_delete.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
