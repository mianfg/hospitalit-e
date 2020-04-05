from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as do_login
from django.shortcuts import render, redirect
from hospitalite.models import Voluntario
from django.core.exceptions import ObjectDoesNotExist

def index(request):
    # Creamos el formulario de autenticación vacío
    form = AuthenticationForm()
    if request.method == "POST":
        # Añadimos los datos recibidos al formulario
        form = AuthenticationForm(data=request.POST)
        # Si el formulario es válido...
        if form.is_valid():
            # Recuperamos las credenciales validadas
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # Verificamos las credenciales del usuario
            user = authenticate(username=username, password=password)

            # Si existe un usuario con ese nombre y contraseña
            if user is not None:
                try:
                    voluntario = Voluntario.objects.get(username=username)
                    if voluntario is not None:
                        if not voluntario.verificado:
                            return render(request, "login.html", {'form': form, 'error_login': True}) 
                except ObjectDoesNotExist:
                    pass

                
                # Hacemos el login manualmente
                do_login(request, user)
                # Y le redireccionamos a la portada
                return redirect('/modificar_datos')

    # Si llegamos al final renderizamos el formulario
    return render(request, "login.html", {'form': form, 'error_login': False})