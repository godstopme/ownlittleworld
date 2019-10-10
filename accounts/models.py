from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
from django.utils.translation import gettext_lazy


class User(AbstractUser):
    email = models.EmailField(gettext_lazy('email address'), null=False, blank=True, unique=True)
    username = models.CharField(max_length=16, null=False, blank=False, unique=True)
