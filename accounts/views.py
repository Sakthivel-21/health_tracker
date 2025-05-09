from django.shortcuts import render
from rest_framework.views import APIView

from rest_framework import viewsets
from django.contrib.auth import get_user_model
from rest_framework import generics, permissions
from .models import *
from accounts.serializers import *
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
User = get_user_model()

class RegistrationView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get_permissions(self):
        if self.action=='create':
            return [AllowAny()]
        return super().get_permissions()
        

    @action(detail=False, methods=['POST'], permission_classes=[IsAuthenticated])
    def logout(self, request):
        request.user.auth_token.delete()
        return Response({'message': 'User Logged Out'}, status=status.HTTP_200_OK)

class LoginView(viewsets.ViewSet):
    permission_classes=[AllowAny]
    def create(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=status.HTTP_200_OK)


class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    Retrieve and update user profile details.
    """
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class UserHealthView(viewsets.ModelViewSet):
    serializer_class = UserHealthSerializer
    permission_classes = [permissions.IsAuthenticated]
    

    def get_queryset(self):
        user = self.request.user
        return UserHealth.objects.filter(user=user)
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.user != request.user:
            return Response({"detail": "Unauthorized"}, status=status.HTTP_403_FORBIDDEN)
        return super().partial_update(request, *args, **kwargs)
    
    

    
    
    
    
