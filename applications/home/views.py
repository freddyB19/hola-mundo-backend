from django.contrib.auth import login, logout, authenticate, get_user_model
from django.db.models import Count, Q

from rest_framework import views, generics, response, status
from rest_framework.decorators import api_view

from . import serializers, models, session_user, paginations, permissions

# Create your views here.

class NewPlayerCreateAV(generics.CreateAPIView):
    serializer_class = serializers.PersonSerializer


class LoginUserAV(views.APIView):
    def post(self, request, format=None):
        data_response = {}
        nombre = request.data.get("nombre", None)
        apellido = request.data.get("apellido", None)

        if models.Person.objects.filter(nombre = nombre, apellido = apellido).exists():
            progreso = models.ProgresoPerson.objects.select_related("person").get(
                person__nombre = nombre,
                person__apellido = apellido
            )

            user = session_user.User(request)
            user.login_user(user = progreso.person)
            user.add(
                puntos = progreso.puntos,
                actual = progreso.url,
                next = progreso.next
            )
            data_response = user.get()

            return response.Response(data_response, status = status.HTTP_200_OK)
        data_response["errors"] = "Credenciales Invalidas"
        return response.Response(data_response, status = status.HTTP_400_BAD_REQUEST)


class LogoutUserAV(views.APIView):

    def post(self, request, format = None):
        user = session_user.User(request)
        response_user = {}

        data = user.logout_user() or {"errors": "El usuario ya se encuentra fuera de sesion."}
        if "errors" in data:
            return response.Response(data, status = status.HTTP_400_BAD_REQUEST)
        return response.Response(status = status.HTTP_204_NO_CONTENT)



class ProgresoPersonListAV(generics.ListAPIView):
    pagination_class = paginations.ProgresoPersonPagination
    serializer_class = serializers.ProgresoPersonSerializer
    #lookup_url_kwarg = "pk"

    def get_queryset(self):
        data = {self.lookup_field: self.kwargs[self.lookup_field]}
        return models.ProgresoPerson.objects.filter(person__pk = self.kwargs.get("pk")) #



class ModuloListAV(generics.ListAPIView):
    serializer_class = serializers.ModuloSerializer

    def get_queryset(self):
        return models.Modulo.objects.annotate(count = Count("modulo_sesion")).order_by("num_modulo", "id")


class ModuloDetailAV(generics.RetrieveAPIView):
    queryset =  models.Modulo.objects.all()
    serializer_class = serializers.ModuloDetalleSerializer
    permission_classes = [permissions.IsUserAccessModuloOrRedirect]


class SesionDetailAV(generics.RetrieveAPIView):
    queryset = models.Sesion.objects.all()
    serializer_class = serializers.SesionSerializer
    permission_classes = [permissions.IsUserAccessSesionDetailOrRedirect]



@api_view(["POST",])
def next_level_player(request):
    if request.method == "POST":
        if request.data.get("data", False) and request.data.get("player", False):
            if session_user.User(request).get():
                user = session_user.User(request)
                data = user.get()

                if models.Sesion.objects.filter(checkpoint = data["player"]["puntos"] + 16).exists():
                    next_url = models.Sesion.objects.get(checkpoint = data["player"]["puntos"] + 16).get_absolute_url()
                else:
                    next_url = ""

                progreso = models.ProgresoPerson(
                    person = models.Person.objects.get(pk = data["data"]["id"]),
                    puntos = data["player"]["puntos"] + 8,
                    url = data["player"]["next"],
                    next = next_url
                )
                if progreso.is_winner():
                    return response.Response({"win":"has ganado"}, status = status.HTTP_200_OK)

                user.update(
                    puntos = progreso.puntos,
                    actual = progreso.url,
                    next = progreso.next
                )
                progreso.save()
                return response.Response(user.get())
            return response.Response({"access":"Se requiere Login o no se recibió los datos correctos."}, status = status.HTTP_204_NOT_CONTENT)
        return response.Response({"access":"No data"}, status = status.HTTP_400_BAD_REQUEST)




"""

@api_view(["GET",])
def get_view(request):
    if request.method == "GET":
        user = session_user.User(request)
        return response.Response(user.get())


@api_view(["GET",])
def get_modulos_list(request):
    if request.method == "GET":
        modulos = models.Modulo.objects.annotate(count = Count("modulo_sesion")).order_by("num_modulo", "id")
        serializer = serializers.ModuloSerializer(modulos, many = True)
        return response.Response(serializer.data, status = status.HTTP_200_OK)


@api_view(["GET",])
def get_modulo_detail(request, pk = None):
    if request.method == "GET":
        if models.Modulo.objects.filter(pk = pk).exists():
            modulo = models.Modulo.objects.get(pk = pk)
            serializer = serializers.ModuloDetalleSerializer(modulo, context = {"request": request})
            return response.Response(serializer.data, status = status.HTTP_200_OK)
        return response.Response({"errors": "Error"}, status = status.HTTP_400_BAD_REQUEST)

@api_view(["GET",])
def get_sesion_detail(request, pk = None):
    if request.method == "GET":
        if models.Sesion.objects.filter(pk = pk).exists():
            sesion = models.Sesion.objects.get(pk = pk)
            serializer = serializers.SesionSerializer(sesion)
            return response.Response(serializer.data, status = status.HTTP_200_OK)
        return response.Response({"errors": "Error"}, status = status.HTTP_400_BAD_REQUEST)



@api_view(["POST",])
def logout_view(request):
    if request.method == "POST":
        user = session_user.User(request)
        response_user = {}
        data = user.logout_user() or {"errors": "El usuario ya se encuentra fuera de sesion."}
        return response.Response(data)



@api_view(["POST",])
def new_person(request):
    data = {}
    if request.method == "POST":
        serializer = serializers.PersonSerializer(data = request.data)
        if serializer.is_valid():
            person = serializer.save()
            data["person"] = {
                "id": person.id,
                "name": person.nombre,
                "last_name": person.apellido,
                "edad": person.edad
            }
            return response.Response(data, status.HTTP_201_CREATED)
        data["errors"] = "Datos Invalidos"
        return response.Response(data, status = status.HTTP_400_BAD_REQUEST)

@api_view(["POST",])
def login_view(request):
    if request.method == "POST":
        data = {}
        nombre = request.data.get("nombre", None)
        apellido = request.data.get("apellido", None)

        if models.Person.objects.filter(nombre = nombre, apellido = apellido).exists():
            data = models.ProgresoPerson.objects.select_related("person").get(
                person__nombre = nombre,
                person__apellido = apellido
            )

            user = session_user.User(request)
            user.login_user(user = data.person)
            user.add(
                puntos = data.puntos,
                actual = data.url,
                next = data.next
            )
            response_user = user.get()

            return response.Response(response_user, status = status.HTTP_200_OK)
        data["errors"] = "Credenciales Invalidas"
        return response.Response(data, status = status.HTTP_400_BAD_REQUEST)
"""
