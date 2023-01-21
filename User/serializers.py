# serializers.py
from rest_framework import serializers

from .models import User

from django.contrib.auth.hashers import make_password


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User"""

    class Meta:
        """Fields to be serialized"""
        model = User
        fields = ("id", "username", "password", "first_name", "last_name", 
                  "email", "is_staff", "is_active", "is_manager", "account",
                  "phone", "address",
                )

        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))
        return super(UserSerializer, self).create(validated_data)

    # def create(self, validated_data):
    #     password = validated_data.pop('password')
    #     user_obj = User(**validated_data)
    #     user_obj.set_password(password)
    #     user_obj.save()
    #     return user_obj
