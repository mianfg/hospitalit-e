from django.shortcuts import render, redirect
from hospitalite.forms import UsuarioCreacionForm
from hospitalite.models import Usuario
import random
import re

# Create your views here.
def index(response):
    pattern_dni= re.compile("^[0-9]{8,8}[A-Za-z]$")
    pattern_nie= re.compile("^[a-zA-Z]\d{7}[a-zA-Z]$")

    if response.method == "POST":
        form = UsuarioCreacionForm(response.POST)
        data = response.POST.copy()
        if not pattern_dni.match(data.get('dni')) and not pattern_nie.match(data.get('dni')):
            return render(response, "registro.html", {"form":form, "error": "Introduzca un DNI o NIE correctos"})
        if Usuario.objects.filter(dni=data.get('dni')).exists():
            return render(response, "registro.html", {"form":form, "error": "El DNI o NIE ya existe"})
        if Usuario.objects.filter(username=data.get('username')).exists():
            return render(response, "registro.html", {"form":form, "error": "El nombre de usuario ya existe"})
        if data.get('password1') != data.get('password2'):
            return render(response, "registro.html", {"form":form, "error": "Las contraseñas no coinciden"})
    
        if form.is_valid():
            u = form.save(commit=False)
            u.save()

        return redirect("/login")
    else:
        form = UsuarioCreacionForm()

    return render(response, "registro.html", {"form":form, "error": None})