from django.contrib import admin
from hospitalite.models import Usuario
from hospitalite.models import Voluntario
from hospitalite.models import Match
from hospitalite.models import Rating

admin.site.register(Usuario)
admin.site.register(Voluntario)
admin.site.register(Match)
admin.site.register(Rating)