from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.db import models
import uuid


class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)  # Champ de mot de passe
    age = models.PositiveIntegerField(null=True, blank=True)

    can_be_contacted = models.BooleanField(default=False)
    can_be_shared = models.BooleanField(default=False)

    email_confirmed = models.BooleanField(default=False)
    email_confirm_token = models.UUIDField(default=uuid.uuid4)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username
