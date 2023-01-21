from django.contrib.auth import authenticate, get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.authtoken.models import Token
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import (HTTP_200_OK, HTTP_400_BAD_REQUEST,
                                   HTTP_404_NOT_FOUND)

from Common.custom_response import custom_response
from .models import User
from .serializers import UserSerializer


# Create your views here.

User = get_user_model()

class LoginView(viewsets.ViewSet):
    """User Login View"""
    def post(self, request):
        """Login Method"""
        username = request.data.get("username")
        password = request.data.get("password")
        if username is None or password is None:
            return Response({'error': 'Please provide both username and password'},
                            status=HTTP_400_BAD_REQUEST)
        print(username, password)
        user = authenticate(username=username, password=password)
        if not user:
            return Response({'error': 'Invalid Credentials'},
                            status=HTTP_404_NOT_FOUND)
        print(user,'user')
        token, _ = Token.objects.get_or_create(user=user)
        print(token,'tokem')
        return Response({'token': token.key, 'user_id': user.pk,
                         'username': user.username, 'email': user.email,
                         'created': token.created,
                         'is_admin': user.is_staff,
                         'first_name': user.first_name,
                         }, status=HTTP_200_OK)


class UserSignup(viewsets.ViewSet):
    """User Signup View"""    

    def create(self, request):
        data = request.data.copy()
        # data["locations"] = [int(location) for location in data["locations"].split(",")]
        serializer = UserSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return custom_response(result=serializer.data)

class UserView(viewsets.ViewSet):
    """User CRUD Operations View"""
    # permission_classes = (IsAuthenticated,)

    def list(self, request):
        """Method to Provide List of USERS"""
        queryset = User.objects.filter(is_manager=False)
        paginator = PageNumberPagination()
        paginator.page_size = 100
        page = paginator.paginate_queryset(queryset, request)
        serializer = UserSerializer(page, many=True).data

        return custom_response(result=paginator.get_paginated_response(serializer).data)

    def retrieve(self, request, pk=None):
        item = get_object_or_404(User, pk=pk)
        serializer = UserSerializer(item)
        return custom_response(result=serializer.data)

    def update(self, request, pk=None):
        queryset = User.objects.all()
        instance = get_object_or_404(queryset, pk=pk)
        serializer = UserSerializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return custom_response(result=serializer.data)
        return custom_response(result=serializer.errors)

    def destroy(self, request, pk=None):
        queryset = User.objects.all()
        item = get_object_or_404(queryset, pk=pk)
        item.delete()
        return custom_response(result="user deleted")
