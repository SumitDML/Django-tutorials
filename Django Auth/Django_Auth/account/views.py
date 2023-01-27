from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import UserRegistrationSerializer, UserLoginSerializer, UserProfileSerializer, \
    SendPasswordResetEmailSerializer, UserChangePasswordSerializer, UserPasswordResetSerializer

UserChangePasswordSerializer
from django.contrib.auth import authenticate
from .renderers import UserRenderer
# Create your views here.
from rest_framework_simplejwt.tokens import RefreshToken


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class UserRegistrationView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            return Response({
                'msg': 'Registration Successful!',
            }, status=status.HTTP_201_CREATED)
        return Response({
            'error': serializer.errors,
        }, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            user = authenticate(email=email, password=password)

            if user is not None:
                token = get_tokens_for_user(user)
                return Response({
                    'token': token,
                    'msg': "Login Successful!"
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'errors': {'non_field_errors': ['Email or Password is not Valid']}
                }, status=status.HTTP_403_FORBIDDEN)
        return Response({
            'errors': {'errors': serializer.errors}
        }, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        serializer = UserProfileSerializer(request.user)
        return Response({
            'data': serializer.data,
        }, status=status.HTTP_200_OK)


class UserChangePasswordView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        serializer = UserChangePasswordSerializer(data=request.data, context={'user': request.user})
        if serializer.is_valid(raise_exception=True):
            return Response({
                'msg': 'Password Changed Successfully!'
            }, status=status.HTTP_200_OK)
        return Response({
            'errors': {'errors': serializer.errors}
        }, status=status.HTTP_400_BAD_REQUEST)


class SendPasswordResetEmailView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, format=None):
        serializer = SendPasswordResetEmailSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response({
                'msg': 'Password reset link send! Please check your Email!'
            }, status=status.HTTP_200_OK)
        return Response({
            'errors': {'errors': serializer.errors}
        }, status=status.HTTP_400_BAD_REQUEST)


class UserPasswordResetView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, uid, token, format=None):
        serializer = UserPasswordResetSerializer(data=request.data, context={'uid': uid, 'token': token})
        if serializer.is_valid(raise_exception=True):
            return Response({
                'msg': 'Password reset Successfully!'
            }, status=status.HTTP_200_OK)
        return Response({
            'errors': {'errors': serializer.errors}
        }, status=status.HTTP_400_BAD_REQUEST)
