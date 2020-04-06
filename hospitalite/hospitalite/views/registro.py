from django.shortcuts import render, redirect
from hospitalite.forms import UsuarioCreacionForm
from hospitalite.models import Usuario
import random

# Create your views here.
def index(response):
    if response.method == "POST":
        form = UsuarioCreacionForm(response.POST)
        data = response.POST.copy()
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