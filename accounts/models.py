from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.contrib.auth.hashers import make_password
from simple_history.models import HistoricalRecords
from .validators import validate_mobile_phone, validate_name
from .utils import make_upper_camel_case_names


class CustomUserManager(UserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("Es obligatorio tener un correo electrónico")
        if not password:
            raise ValueError("Es obligatorio tener una clave")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self._create_user(email, password, **extra_fields)


# Create your models here.
class User(AbstractUser):
    first_name = models.CharField(max_length=50, validators=[validate_name, ], verbose_name="Nombre", )
    last_name = models.CharField(max_length=50, validators=[validate_name, ], verbose_name="Apellidos", )
    email = models.EmailField(unique=True, verbose_name="Email", )
    country = models.CharField(max_length=50, validators=[validate_name, ], verbose_name="Pais", )
    city = models.CharField(max_length=50, validators=[validate_name, ], verbose_name="Ciudad", )
    address = models.CharField(max_length=255, verbose_name="Direccion", )
    mobile_phone = models.CharField(max_length=15, unique=True, validators=[validate_mobile_phone, ],
                                    verbose_name="Teléfono movil", )
    username = models.CharField(unique=False, max_length=50)
    history = HistoricalRecords()
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'username', 'country', 'city', 'address', 'mobile_phone', ]

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"

    def __str__(self):
        return f"{self.username}"

    def save(self, *args, **kwargs):
        self.first_name = make_upper_camel_case_names(self.first_name)
        self.last_name = make_upper_camel_case_names(self.last_name)
        self.country = make_upper_camel_case_names(self.country)
        self.city = make_upper_camel_case_names(self.city)
        self.username = self.first_name
        if not self.is_superuser:
            self.password = make_password(self.password)
        super().save(*args, **kwargs)
