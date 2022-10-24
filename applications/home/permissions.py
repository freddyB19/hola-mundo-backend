from rest_framework import permissions

from . import session_user

class IsUserAccessModuloOrRedirect(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        user = session_user.User(request)
        data = user.get()
        return data["player"]["puntos"] >= obj.checkpoint

class IsUserAccessSesionDetailOrRedirect(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        user = session_user.User(request)
        data = user.get()
        return data["player"]["puntos"] >= obj.checkpoint
