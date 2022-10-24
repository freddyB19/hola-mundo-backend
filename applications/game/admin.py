from atexit import register
from django.contrib import admin

from . import models


# Register your models here.
class ModuloAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "title"
    ]

class SesionAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "url",
        "checkpoint"
    ]
    list_filter = ("modulo", "num_sesion")

class ProgresoPlayerAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "user",
    ]


admin.site.register(models.ProgresoPlayer, ProgresoPlayerAdmin)

admin.site.register(models.Modulo, ModuloAdmin)
admin.site.register(models.Sesion, SesionAdmin)
