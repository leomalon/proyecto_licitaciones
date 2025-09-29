"""
We define a custom "User" model to avoid using the
default Django "User" model. This is important, because
the "User" model is referenced everywhere.
"""
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

# Create your models here.

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email must be provided")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)


class Usuario(AbstractBaseUser,PermissionsMixin):
    """
    Custom base model for users
    """
    email = models.EmailField(
        verbose_name="correo electrónico", #Django admin will show this
        unique=True, #No duplicates
        blank=False) #No blank

    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "email"     # Login with email
    REQUIRED_FIELDS = []         # No extra fields required.

    objects = CustomUserManager()

    def __str__(self):
        return self.email

