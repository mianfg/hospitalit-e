from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms.models import model_to_dict, fields_for_model
from .models import Usuario, Voluntario, PROVINCIAS

class UsuarioCreacionForm(UserCreationForm):
    password1 = forms.CharField(
        widget=forms.PasswordInput(),
        min_length=4,
        max_length=8,
        strip=True,
        label="PIN"
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(),
        min_length=4,
        max_length=8,
        strip=True,
        label="Confirme PIN"
    )

    username = forms.CharField(label = "Nombre de usuario")
    dni = forms.CharField(label = "DNI/NIE/Pasaporte")
    edad = forms.IntegerField(min_value=18)
    skype = forms.CharField(label = "Skype", required = False)
    facetime = forms.CharField(label = "Facetime", required = False)

    class Meta:
        model = Usuario
        fields = ('username', 'dni', 'first_name', 'last_name', 'edad', 'provincia', 'localidad', 'skype', 'facetime')

class UsuarioModificacionForm(UserCreationForm):
    password1 = forms.CharField(
        widget=forms.PasswordInput(),
        min_length=4,
        max_length=8,
        strip=True,
        label="PIN"
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(),
        min_length=4,
        max_length=8,
        strip=True,
        label="Confirme PIN"
    )

    first_name = forms.CharField(label = "Nombre", required = True)
    last_name = forms.CharField(label = "Apellidos", required = True)
    skype = forms.CharField(label = "Skype", required = True)
    facetime = forms.CharField(label = "Facetime", required = True)
    edad = forms.IntegerField(required=True)

    class Meta:
        model = Usuario
        fields = ('first_name', 'last_name', 'edad', 'provincia', 'localidad', 'skype', 'facetime')

class VoluntarioCreacionForm(forms.ModelForm):

    consentimiento = forms.BooleanField(required=True)

    class Meta:
        model = Voluntario
        fields = ( 'email', 'telefono', 'ocupacion','consentimiento')