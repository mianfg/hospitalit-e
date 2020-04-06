from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from hospitalite.models import Usuario

@login_required
def index(response):
    user = Usuario.objects.get(username=response.user.username)
    is_voluntario = user.is_voluntario()
    first_name = user.first_name

    text = "Si quieres entrar en contacto con alguien, sólo tienes que pulsar en el siguiente botón, y buscaremos voluntarios disponibles"
    button_text = "Buscar voluntarios"
    search_text = "Estamos buscando voluntarios, espere un momento"

    if is_voluntario:
        text = "Pulsa en el siguiente botón para contactar con un enfermo"
        search_text = "Estamos buscando enfermos, espere un momento"
        button_text = "Contactar con un enfermo"

    items = {
        'is_voluntario' : is_voluntario,
        'first_name'    : first_name,
        'text'          : text,
        'button_text'   : button_text,
        'search_text'   : search_text
    }

    return render(response, "matching.html", items)
