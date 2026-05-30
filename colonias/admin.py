from django.contrib import admin
from .models import Planeta, Colonia, Mision, Informe
# Register your models here.

@admin.register(Planeta)
class PlanetaAdmin(admin.ModelAdmin):

    list_display = ['nombre', 'tipo', 'distancia']

    search_fields = ['nombre']
    
    
@admin.register(Colonia)
class ColoniaAdmin(admin.ModelAdmin):

    list_display = ['nombre', 'poblacion', 'planeta']

    list_filter = ['planeta']

    search_fields = ['nombre']
    
    
@admin.register(Mision)
class MisionAdmin(admin.ModelAdmin):

    list_display = ['titulo', 'estado', 'fecha']

    list_filter = ['estado']

    search_fields = ['titulo']
    
@admin.register(Informe)
class InformeAdmin(admin.ModelAdmin):

    list_display = ['mision', 'fecha']
