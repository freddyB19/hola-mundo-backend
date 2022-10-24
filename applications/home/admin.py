from atexit import register
from django.contrib import admin

from . import models


# Register your models here.
@admin.register(models.Person)
class PersonAdmin(admin.ModelAdmin):

    list_display = [
        "id",
        "nombre"
    ]

class ModuloAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "title"
    ]

class SesionAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "url"
    ]
    list_filter = ("modulo", "num_sesion")

class ProgresoPersonAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "person",
        "url"
    ]


admin.site.register(models.ProgresoPerson, ProgresoPersonAdmin)

admin.site.register(models.Modulo, ModuloAdmin)
admin.site.register(models.Sesion, SesionAdmin)
