from django.contrib.auth import logout as do_logout
from django.shortcuts import render, redirect

def index(request):
    # Finalizamos la sesión
    do_logout(request)
    # Redireccionamos a la portada
    return redirect('/')