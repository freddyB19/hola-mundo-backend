from rest_framework import permissions

from . import session

class IsPlayerAccessModuloOrRedirect(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        user = session.User(request)
        data = user.get()
        return data["player"]["puntos"] >= obj.checkpoint

class IsPlayerAccessSesionDetailOrRedirect(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        user = session.User(request)
        data = user.get()
        return data["player"]["puntos"] >= obj.checkpoint
