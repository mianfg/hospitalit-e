from django.shortcuts import render, redirect
from hospitalite.forms import UsuarioCreacionForm
from hospitalite.models import Usuario
import random

# Create your views here.
def index(response):
    if response.method == "POST":
        form = UsuarioCreacionForm(response.POST)
        if form.is_valid():
            u = form.save(commit=False)
            u.username = random.randint(10, 999999)
            u.save()

        return redirect("/registro")
    else:
        form = UsuarioCreacionForm()

    return render(response, "registro.html", {"form":form})