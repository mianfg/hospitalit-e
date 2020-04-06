from django.shortcuts import render, redirect
from hospitalite.forms import VoluntarioCreacionForm, UsuarioCreacionForm
from hospitalite.models import Usuario, Voluntario
import random

# Create your views here.
def index(response):
    if response.method == "POST":
        usuario_form = UsuarioCreacionForm(response.POST)
        voluntario_form = VoluntarioCreacionForm(response.POST)
        data = response.POST.copy()

        if Usuario.objects.filter(username=data.get('username')).exists():
            return render(response, "registro_voluntario.html", {'usuario_form': usuario_form, 'voluntario_form': voluntario_form,"error": "El nombre de usuario ya existe"})
        if data.get('password1') != data.get('password2'):
            return render(response, "registro_voluntario.html", {'usuario_form': usuario_form, 'voluntario_form': voluntario_form, "error": "Las contraseñas no coinciden"})
        if not data.get('consentimiento'):
            return render(response, "registro_voluntario.html", {'usuario_form': usuario_form, 'voluntario_form': voluntario_form, "error": "Debe aceptar los términos y condiciones"})

        if usuario_form.is_valid() and voluntario_form.is_valid():
            usuario = usuario_form.save()
            voluntario = voluntario_form.save(commit=False)      
            voluntario.username = usuario
            voluntario.save()
            return redirect("/login")

        else:
            context = {
                'usuario_form': usuario_form,
                'voluntario_form': voluntario_form,
                'error':None
            }

    else:
        context = {
            'usuario_form': UsuarioCreacionForm(),
            'voluntario_form': VoluntarioCreacionForm(),
            'error':None
        }

    return render(response, 'registro_voluntario.html', context)