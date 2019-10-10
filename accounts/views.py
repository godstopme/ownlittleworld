from django.contrib.auth import get_user_model
from rest_framework import viewsets, mixins, permissions

from accounts.serializers import UserSignupSerializer


class SignupUserViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = get_user_model().objects
    serializer_class = UserSignupSerializer
