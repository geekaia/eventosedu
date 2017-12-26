from django.contrib import admin

# Register your models here.
from .models import *

class PerfilAdmin(admin.ModelAdmin):

    search_fields = ['nomecracha', 'user__first_name', 'email', ]
    list_display = ('user', 'nomecompleto', 'nomecracha','email', 'completado')


admin.site.register(Perfil, PerfilAdmin)

