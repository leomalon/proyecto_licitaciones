"""
We define a custom "User" model to avoid using the
default Django "User" model. This is important, because
the "User" model is referenced everywhere.
"""
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import RegexValidator
from django.db import models

# Create your models here.

class CustomUserManager(BaseUserManager):
    """
    Custom manager extending Django's BaseUserManager.
    
    This manager handles the creation of the users. 
    """
    def create_user(self, email,password=None, **extra_fields):
        """
        Function that creates a normal user.
        """
        if not email:
            raise ValueError("No se encontró ningún email")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Function that creates an admin user.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)

class Usuario(AbstractBaseUser,PermissionsMixin):
    """
    Custom user model extending Django's AbstractBaseUser.

    This model uses email as the primary identifier instead of username
    and optionally stores a RUC.

    Fields:
        email (EmailField): Unique email used for authentication.
        ruc (CharField): Optional 11-digit numeric RUC shared between clients and providers.
        is_active (BooleanField): Whether the account is active.
        is_staff (BooleanField): Grants access to Django admin.
    """
    email = models.EmailField(
        verbose_name="correo electrónico", #Django admin will show this
        unique=True, #No duplicates
        blank=False) #No blank
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "email" # Use email as the unique login field
    REQUIRED_FIELDS = []     # Extra fields required when creating a user via createsuperuser

    objects = CustomUserManager() #Reference to the manager.

    def __str__(self): #pylint: disable=E0307
        """
        Returns the object as a readable string.
        """
        return self.email

class BasePerfil(models.Model):
    """
    Abstract class to share common fields between
    "Cliente" and "Proveedor".
    """
    ruc = models.CharField(verbose_name="RUC usuario",
        max_length=11,
        validators=[
            RegexValidator(
                regex=r'^\d{11}$', #Exactly 11 numbers in the string.
                message="El RUC debe contener exactamente 11 dígitos numéricos."
            )
        ],
        blank=False, #No blank
        unique=True  # No duplicates
    )
    pais = models.CharField(max_length=100)
    departamento = models.CharField(max_length=100)
    provincia = models.CharField(max_length=100)
    direccion_comercial = models.CharField(max_length=255)
    razon_social = models.CharField(max_length=255)
    actividad_comercial = models.CharField(max_length=255)
    nombre_comercial = models.CharField(max_length=255)
    nombre_contacto = models.CharField(max_length=150)
    telefono_movil = models.CharField(max_length=20)
    cargo = models.CharField(max_length=100)

    usuario = models.OneToOneField(
        Usuario,
        on_delete=models.CASCADE,
        related_name="%(class)s_profile" # "cliente_profile" o "proveedor_profile"
    )

    class Meta:
        """
        We use it to add the variable abstract = True, so
        it does not get created in the DB.
        """
        abstract = True