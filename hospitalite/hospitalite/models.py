from django.db import models
from django import forms
from django.contrib.auth.models import AbstractUser

class Usuario (AbstractUser):
    # Código de usuario generado
    username = models.CharField(max_length = 6, unique = True)
    first_name = models.CharField(max_length = 20)
    last_name = models.CharField(max_length = 60)
    provincia = models.CharField(max_length = 10)
    localidad = models.CharField(max_length = 20)
    skype = models.CharField(max_length = 15)
    facetime = models.CharField(max_length = 20)
    edad = models.IntegerField()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username
