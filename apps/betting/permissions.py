from rest_framework import permissions


class IsPlayer(permissions.BasePermission):
    def has_permission(self, request, view):
        # Check if the user is a player

        return request.user.is_authenticated and hasattr(request.user, "player")
