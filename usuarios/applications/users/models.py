from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    GENDER_CHOICES = (
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('O', 'Otros'),
    )
    objects = UserManager()
    is_staff = models.BooleanField(default=False)

    username = models.CharField("username", max_length=15, unique=True)
    email = models.EmailField("Email")
    nombres = models.CharField("Nombres", max_length=30, blank=True)
    apellidos = models.CharField("Apellidos", max_length=30, blank=True)
    genero = models.CharField("Genero", max_length=1,
                              choices=GENDER_CHOICES, blank=True)

    codregistro = models.CharField(max_length=6, blank=True)
    is_active = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def get_short_name(self):
        return self.username

    def get_full_name(self):
        print(self.nombres)
        return self.nombres + ' ' + self.apellidos
