from helpers.error_response import custom_error_msg
from .serializers import ResetPasswordSerializer, SendResetPasswordCodeSerializer, UserLoginSerializer, UserSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,  AllowAny
from rest_framework.views import APIView
from rest_framework import status 
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.generics import GenericAPIView
from django.db.models import Q
from django.contrib.auth import authenticate



class UserCreateView(GenericAPIView):
    """
    class to create user
    """
    permission_classes = [AllowAny]
    serializer_class = UserSerializer
    def post(self, request, format=None): 
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            qs = serializer.save()            
            data = {"code" : status.HTTP_201_CREATED, "status": 'Success', 'message':'User successfully registered','data':self.get_serializer(qs).data}          
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            error = custom_error_msg(serializer.errors)         
            data = {"code" : status.HTTP_400_BAD_REQUEST, "status": 'Failed','message':error}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(GenericAPIView):
    """
    class to login user
    """
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer
    def post(self, request, format=None): 
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']           
            password = serializer.validated_data['password']  
            user = authenticate(username=username, password=password)
            refresh = RefreshToken.for_user(user)
            access = refresh.access_token    
            user = UserSerializer(user).data  
            data = {"code" : status.HTTP_201_CREATED, "status": 'Success','message':'Login Successful', 'user':user, 'access':str(access), 'refresh':str(refresh)}   
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            error = custom_error_msg(serializer.errors)
            data = {"code" : status.HTTP_400_BAD_REQUEST, "status": 'Failed','message':error}       
            return Response(data, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordCodeView(generics.CreateAPIView):
    """
    class to send reset code to email
    """
    serializer_class = SendResetPasswordCodeSerializer
    permission_classes = [AllowAny]


    def post(self, request, format=None):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():  
            serializer.save()          
            data = {"code" : status.HTTP_201_CREATED, "status": 'Success','message':'Code has been sent to your email'}   
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            error = custom_error_msg(serializer.errors)
            data = {"code" : status.HTTP_400_BAD_REQUEST, "status": 'Failed','message':error}       
            return Response(data, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordView(generics.CreateAPIView):
    """
    class to reset password with code sent to email
    """
    serializer_class = ResetPasswordSerializer
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():  
            serializer.save()          
            data = {"code" : status.HTTP_201_CREATED, "status": 'Success','message':'Password has been successfully changed'}  
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            error = custom_error_msg(serializer.errors)
            data = {"code" : status.HTTP_400_BAD_REQUEST, "status": 'Failed','message':error}       
            return Response(data, status=status.HTTP_400_BAD_REQUEST)


