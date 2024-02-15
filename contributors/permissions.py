from rest_framework.permissions import BasePermission

from projects.models import Project


class IsProjectAuthor(BasePermission):
    """
    Permission qui permet seulement à l'auteur du projet d'ajouter ou de supprimer
    des contributeurs.
    """
    def has_permission(self, request, view):
        # Vérifie si l'utilisateur est l'auteur du projet
        project_id = request.parser_context['kwargs'].get('project_id')
        if project_id:
            project = Project.objects.get(pk=project_id)
            return project.author == request.user
        return False

    def has_object_permission(self, request, view, obj):
        # Vérifie si l'utilisateur est l'auteur du projet
        return obj.project.author == request.user
