from typing import Any, Dict

from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import AbstractBaseUser
from rest_framework import serializers, fields


class UserSignupSerializer(serializers.ModelSerializer):
    password = fields.CharField(write_only=True, required=True)

    class Meta:
        model = get_user_model()
        fields = (
            'username',
            'email',
            'password',
        )

    def create(self, validated_data: Dict[str, Any]):
        user: AbstractBaseUser = get_user_model()(**validated_data)

        user.set_password(validated_data['password'])
        user.save()

        return user
