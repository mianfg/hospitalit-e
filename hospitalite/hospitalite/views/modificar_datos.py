from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from hospitalite.forms import UsuarioCreacionForm, UsuarioModificacionForm
from hospitalite.models import Usuario

@login_required
def index(response):
    if response.method == "POST":
        form = UsuarioModificacionForm(response.POST, instance = Usuario.objects.get(username=response.user.username))
        if form.is_valid():
            user = form.save(commit=False)

        return redirect("/")
    else:
        form = UsuarioModificacionForm()

    return render(response, "modificar_datos.html", {"form":form})