from django.db import models
from django import forms
from django.contrib.auth.models import AbstractUser
from phone_field import PhoneField

class Usuario (AbstractUser):
    # Código de usuario generado
    username = models.CharField(max_length = 6, primary_key=True)
    dni = models.CharField(max_length=9)
    first_name = models.CharField(max_length = 20, verbose_name="nombre")
    last_name = models.CharField(max_length = 60, verbose_name="apellidos")
    provincia = models.CharField(max_length = 10)
    localidad = models.CharField(max_length = 20)
    skype = models.CharField(max_length = 15)
    facetime = models.CharField(max_length = 20)
    edad = models.IntegerField(default=-1)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username

class Voluntario(models.Model):
    username = models.OneToOneField(Usuario, on_delete=models.CASCADE, primary_key = True)
    email = models.EmailField()
    telefono = PhoneField()
    ocupacion = models.CharField(max_length = 20)
    consentimiento = models.BooleanField()
    verificado = models.BooleanField(default=False)

class Match(models.Model):
    id = models.AutoField(primary_key=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    username1 = models.ForeignKey(Usuario, on_delete=models.DO_NOTHING, related_name='usuario1')
    username2 = models.ForeignKey(Usuario, on_delete=models.DO_NOTHING, related_name='usuario2')
    puntuacion1 = models.IntegerField()
    puntuacion2 = models.IntegerField()

class Feedback(models.Model):
    id_match = models.ForeignKey(Match, on_delete=models.DO_NOTHING)
    username = models.ForeignKey(Usuario, on_delete=models.DO_NOTHING)
    timestamp = models.DateTimeField(auto_now_add=True)
    estrellas = models.IntegerField()
    comentarios = models.CharField(max_length=140)

    class Meta:
        unique_together = (("id_match", "username"),)