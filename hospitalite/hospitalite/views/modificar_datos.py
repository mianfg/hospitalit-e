from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from hospitalite.forms import VoluntarioModificacionForm, UsuarioModificacionForm
from hospitalite.models import Usuario, Voluntario
from django.contrib.auth import login as do_login

@login_required
def index(response):
    user = Usuario.objects.get(username=response.user.username)
    
    is_voluntario = user.is_voluntario()

    usuario_form = UsuarioModificacionForm(instance=user)
    usuario_form.fields['username'].disabled = True
    usuario_form.fields['dni'].disabled = True
    
    if is_voluntario:
        voluntario = Voluntario.objects.get(username=response.user.username)
        voluntario_form = VoluntarioModificacionForm(instance=voluntario)
    else:
        voluntario_form = None

    if response.method == "POST":
        usuario_form = UsuarioModificacionForm(response.POST, instance=user)
        if is_voluntario:
            voluntario_form = VoluntarioModificacionForm(response.POST, instance=voluntario)
        
        data = response.POST.copy()

        if data.get('password1') != data.get('password2'):
            return render(response, "modificar_datos.html", {'usuario_form': usuario_form, 'voluntario_form': voluntario_form, "error": "Las contraseñas no coinciden"})
        
        if usuario_form.is_valid() and voluntario_form.is_valid():
            usuario = usuario_form.save()
            voluntario = voluntario_form.save(commit=False)      
            voluntario.username = usuario
            voluntario.consentimiento = True
            voluntario.save()
            do_login(response, user)
            return redirect("/matching")

        else:
            context = {
                'usuario_form': usuario_form,
                'voluntario_form': voluntario_form,
                'error': "Por favor rellene todos los datos"
            }

    else:
        context = {
            'usuario_form': usuario_form,
            'voluntario_form': voluntario_form,
            'error':None
        }

    return render(response, 'modificar_datos.html', context)