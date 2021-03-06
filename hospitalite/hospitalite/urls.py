"""hospitalite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from hospitalite.views import home
from hospitalite.views import registro
from hospitalite.views import login
from hospitalite.views import logout
from hospitalite.views import modificar_datos
from hospitalite.views import registro_voluntario
from hospitalite.views import matching

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home.index, name="home"),
    path('registro/', registro.index, name="registro"),
    path('registro_voluntario/', registro_voluntario.index, name="registro_voluntario"),
    path('login/', login.index, name="login"),
    path('logout/', logout.index, name="logout"),
    path('modificar_datos/', modificar_datos.index, name="modificar_datos"),
    path('matching/', matching.index, name="matching")
]
