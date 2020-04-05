from django.shortcuts import render, redirect
from hospitalite.forms import VoluntarioCreacionForm, UsuarioCreacionForm
from hospitalite.models import Usuario, Voluntario
import random

# Create your views here.
def index(response):
    if response.method == "POST":
        usuario_form = UsuarioCreacionForm(response.POST)
        voluntario_form = VoluntarioCreacionForm(response.POST)

        if usuario_form.is_valid() and voluntario_form.is_valid():
            usuario = usuario_form.save()
            voluntario = voluntario_form.save(commit=False)      
            voluntario.username = usuario
            voluntario.save()
            return redirect("/")

        else:
            context = {
                'usuario_form': usuario_form,
                'voluntario_form': voluntario_form,
            }

    else:
        context = {
            'usuario_form': UsuarioCreacionForm(),
            'voluntario_form': VoluntarioCreacionForm(),
        }

    return render(response, 'registro_voluntario.html', context)