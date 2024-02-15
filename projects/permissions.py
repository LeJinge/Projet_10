from rest_framework.permissions import BasePermission


class IsAuthor(BasePermission):
    """
    Permission qui permet seulement à l'auteur du projet
    de le modifier ou le supprimer.
    """
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user
