from django.urls import path
from . import views

urlpatterns = [
    path("player/next-level/", views.next_level_player, name = 'player-next-level'),
    path("player/progreso-detail/<pk>/", views.ProgresoPlayerListAV.as_view(), name = 'player-detail-progreso'),

    path("sesion-detail/<int:pk>/", views.SesionDetailAV.as_view(), name = "sesion-detail"),

    path("modulos-list/", views.ModuloListAV.as_view(), name = "modulos-list"),
    path("modulos-detail/<int:pk>/", views.ModuloDetailAV.as_view(), name = "modulos-detail"),

]
