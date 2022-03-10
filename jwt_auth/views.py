from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied, NotFound
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from django.conf import settings
from datetime import datetime, timedelta
import jwt
from .serializers.common import RegisterSerializer, ProfileSerializer, DMSerializer, ProfileEditSerializer

User = get_user_model()

class RegisterView(APIView):
    
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({ 'message': 'Registration successful' })
        
        return Response(serializer.errors, status=422)

class LoginView(APIView):
    
    def get_user(self, username):
        try:
            return User.objects.get(username=username)
        except:
            raise PermissionDenied({ 'message': 'Invalid credentials' })
        
    def post(self, request):
        
        username = request.data.get('username')
        password = request.data.get('password')
        
        user = self.get_user(username)
        if not user.check_password(password):
            raise PermissionDenied({ 'message': 'Invalid credentials' })
        
        login_time = datetime.now() + timedelta(days=3)
        
        token = jwt.encode({ 'sub': user.id, 'exp': int(login_time.strftime('%s')) }, settings.SECRET_KEY, algorithm='HS256')
        return Response({ 'token': token, 'message': f'Welcome {user.username}.' })
    

class UserListView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = ProfileSerializer
    
class UserDetailView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = ProfileSerializer
    
class ProfileView(APIView):
    permission_class = (IsAuthenticated,)
    
    def get(self, request):
        serial = ProfileSerializer(request.user)
        return Response(serial.data, status=status.HTTP_200_OK)
    

class EditProfileView(UpdateAPIView):
    permission_classes = (IsAuthenticated,)

    queryset = User.objects.all()
    serializer_class = ProfileEditSerializer  
class UserFollowView(UpdateAPIView):
    permission_class = (IsAuthenticated,)
    
    def post(self, request, user_pk):
        try:
            user_follow = User.objects.get(pk=user_pk)
        except User.DoesNotExist:
            raise NotFound()
        
        if request.user in user_follow.followed_by.all():
            user_follow.followed_by.remove(request.user.id)
        else:
            user_follow.followed_by.add(request.user.id)
            
        serial = ProfileSerializer(user_follow)
        return Response(serial.data, status=status.HTTP_202_ACCEPTED)
    
class UserMessageCreateView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    
    def post(self, request, recipient_pk):
        request.data['send'] = request.user.id
        request.data['recipient'] = recipient_pk
        serial = DMSerializer(data=request.data)
        try:
            serial.is_valid()
            serial.save()
            return Response(serial.data, status=status.HTTP_201_CREATED)
        except:
            return Response(serial.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
            
            