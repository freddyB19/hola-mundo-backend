from django.utils import timezone
from django.contrib import auth
from django.db.models import Q
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse, reverse_lazy
from rest_framework import response, status, views, generics, parsers
from rest_framework_simplejwt.tokens import RefreshToken

from applications.game.apiv1 import session
from applications.game.models import ProgresoPlayer
from applications.users.models import UserProfile

from . import serializers

@api_view(["POST",])
def validated_UsernameEmail_exists(request):
    if request.method == "POST":
        if request.data.get("username", False) or request.data.get("email", False):
            if UserProfile.objects.filter(Q(username = request.data.get("username")) | Q(email = request.data.get("email")) ).exists():
                return response.Response({"error": "Ya existe un registro con ese username"}, status = status.HTTP_404_NOT_FOUND)
            return response.Response({"message": "OK"}, status = status.HTTP_200_OK)
    return response.Response(status = status.HTTP_400_BAD_REQUEST)


@api_view(["POST",])
def register_user(request):
    if request.method == "POST":
        serializer = serializers.UserProfileRegister(data = request.data)
        data = {}
        if serializer.is_valid():
            result = serializer.save()
            # print(serializer.data)
            data["response"] = "Usuario creado con exito"
            return response.Response(data, status = status.HTTP_201_CREATED)
        data = serializer.errors
        return response.Response(data, status = status.HTTP_400_BAD_REQUEST)


@api_view(["POST",])
def login_view(request):
    data = {}
    if request.method == "POST":
        email = request.data.get("email")
        password = request.data.get("password")

        account = auth.authenticate(email = email, password = password)

        if account is not None:
            user = session.User(request)
            user.login_user(account)
            progreso = account.person_user.values("puntos", "url", "next").last()
            user.add(
                puntos = progreso.get("puntos"),
                actual = progreso.get("url"),
                next = progreso.get("next")
            )
            data_player = user.get()

            data = serializers.UserProfileSerializer2(account).data
            if(account.image):
                data["image"] = f"{request.META['wsgi.url_scheme']}://{request.get_host()}{account.image.url}"
            data["response"] = "Bienvenido"
            data["time"] = serializers.UserProfileDateTimeData(account).data
            data["time"]["last_login"] = timezone.now()
            data["player"] = data_player["player"].copy()

            refresh = RefreshToken.for_user(account)
            data["token"] = {
                "refresh": str(refresh),
                "access": str(refresh.access_token)
            }

            return response.Response(data, status = status.HTTP_200_OK)

        data["error"] = f"Credenciales Invalidas"
        return response.Response(data, status = status.HTTP_400_BAD_REQUEST)

@api_view(["POST",])
def logout_view(request):
    if request.method == "POST":
        user = session.User(request)
        data = user.logout_user()
        return response.Response(status = status.HTTP_204_NO_CONTENT)
