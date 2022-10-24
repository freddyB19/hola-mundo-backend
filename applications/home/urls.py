from django.urls import path
from . import views

urlpatterns = [
    # path("person/add/", views.new_person, name = 'person-add'),
    path("person/add/", views.NewPlayerCreateAV.as_view(), name = 'person-add'),
    path("login-person/", views.LoginUserAV.as_view(), name = 'login-person'),
    #path("login-person/", views.login_view, name = 'login-person'),
    #path("logout-person/", views.logout_view, name = 'logout-person'),
    path("logout-person/", views.LogoutUserAV.as_view(), name = 'logout-person'),

    #path("person/", views.get_view, name = 'person'),

    path("person/next-level/", views.next_level_player, name = 'person-next-level'),
    path("person/progreso-list/<pk>/", views.ProgresoPersonListAV.as_view(), name = 'person-list-progreso'),


    #path("sesion-detail/<int:pk>/", views.get_sesion_detail, name = "sesion-detail"),
    path("sesion-detail/<int:pk>/", views.SesionDetailAV.as_view(), name = "sesion-detail"),


    #path("modulos-list/", views.get_modulos_list, name = "modulos-list"),
    path("modulos-list/", views.ModuloListAV.as_view(), name = "modulos-list"),

    #path("modulos-detail/<int:pk>/", views.get_modulo_detail, name = "modulos-detail"),
    path("modulos-detail/<int:pk>/", views.ModuloDetailAV.as_view(), name = "modulos-detail"),


]
