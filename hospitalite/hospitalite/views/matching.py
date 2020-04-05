from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from hospitalite.models import Usuario

@login_required
def index(response):
    user_id = Usuario.objects.get(username=response.user.username)

    return render(response, "matching.html", {'user_id': user_id})
