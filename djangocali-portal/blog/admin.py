from django.contrib import admin
from .models import Categoria, Articulo


@admin.register(Articulo)
class ArticuloAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'autor', 'creado_en', 'estado']
    search_fields = ['titulo', ]

admin.site.register(Categoria)
