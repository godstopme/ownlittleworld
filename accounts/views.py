from django.contrib.auth import get_user_model
from rest_framework import viewsets, mixins, permissions

from accounts.serializers import UserSignupSerializer


class SignupUserViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = get_user_model().objects
    serializer_class = UserSignupSerializer

    # emailhunter restricts me to signup using my regular email, also i don't like to use OAuth
    # so logic to validate email can be placed either here in controller or directly in serializer' validation method
    # same restrictions apply for clearbit, but additional user data upload can be done via
    # another service in background (like celery, etc) or via django signals
    # no need to block user signup here, profile info can be loaded later
