from django.contrib import admin
from .models import ejemplo, empleado, alumno, Categoria, Vehiculo

# Register your models here.
admin.site.register(ejemplo)
admin.site.register(empleado)
admin.site.register(alumno)

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)

@admin.register(Vehiculo)
class VehiculoAdmin(admin.ModelAdmin):
    list_display = (
        'marca',
        'modelo',
        'anio',
        'precio',
        'stock',
        'activo',
        'en_oferta',
        'precio_anterior',
    )

    list_editable = (
        'stock',
        'activo',
        'en_oferta',
        'precio_anterior',
    )

    list_filter = (
        'marca',
        'activo',
        'en_oferta',
        'categoria',
    )

    search_fields = (
        'marca',
        'modelo',
    )

    ordering = ('marca', 'modelo')