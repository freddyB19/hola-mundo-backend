from django.db.models import Count
from rest_framework import views, generics, response, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from rest_framework import permissions as perm

from applications.users.models import UserProfile
from . import serializers, session, paginations, permissions
from applications.game import models



class ProgresoPlayerListAV(generics.ListAPIView):
    pagination_class = paginations.ProgresoPlayerPagination
    serializer_class = serializers.ProgresoPlayerSerializer
    permission_classes = [IsAuthenticated]
    #lookup_url_kwarg = "pk"

    def get_queryset(self):
        data = {self.lookup_field: self.kwargs[self.lookup_field]}
        return models.ProgresoPlayer.objects.filter(user_id = self.kwargs.get("pk")).order_by("-id") #



class ModuloListAV(generics.ListAPIView):
    serializer_class = serializers.ModuloSerializer

    def get_queryset(self):
        return models.Modulo.objects.annotate(count = Count("modulo_sesion")).order_by("num_modulo", "id")


class ModuloDetailAV(generics.RetrieveAPIView):
    queryset =  models.Modulo.objects.all()
    serializer_class = serializers.ModuloDetalleSerializer
    #permission_classes = [permissions.IsPlayerAccessModuloOrRedirect]


class SesionDetailAV(generics.RetrieveAPIView):
    queryset = models.Sesion.objects.all()
    serializer_class = serializers.SesionSerializer
    permission_classes = [IsAuthenticated] #permissions.IsPlayerAccessSesionDetailOrRedirect


@api_view(["POST",])
def next_level_player(request):
    if request.method == "POST":
        if request.data.get("data", False) and request.data.get("player", False):
            user = session.User(request)
            data = user.get()

            if models.Sesion.objects.filter(checkpoint = data["player"]["puntos"] + 16).exists():
                next_url = models.Sesion.objects.get(checkpoint = data["player"]["puntos"] + 16).get_absolute_url()
            else:
                next_url = ""

            progreso = models.ProgresoPlayer(
                user = UserProfile.objects.get(pk = data["data"]["id"]),
                puntos = data["player"]["puntos"] + 8,
                url = data["player"]["next"],
                next = next_url
            )
            user.update(
                puntos = progreso.puntos,
                actual = progreso.url,
                next = progreso.next
            )
            progreso.save()

            if progreso.player_is_winner():
                return response.Response({"win":"has ganado"}, status = status.HTTP_200_OK)

            return response.Response(user.get(), status = status.HTTP_200_OK)
        return response.Response({"access":"No data"}, status = status.HTTP_400_BAD_REQUEST)
