from django.shortcuts import get_object_or_404
from rest_framework.permissions import BasePermission

from contributors.models import Contributor
from projects.models import Project


class IsProjectAuthor(BasePermission):
    """
    Permission qui permet seulement à l'auteur du projet d'ajouter ou de supprimer
    des contributeurs.
    """
    message = "Seul l'auteur du projet peut ajouter ou supprimer des contributeurs."

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        # Pour la méthode POST, récupérez l'ID du projet depuis le corps de la requête
        if request.method == 'POST':
            project_id = request.data.get('project')
            project = get_object_or_404(Project, pk=project_id)
            return project.author == request.user

        # Pour la méthode DELETE, récupérez l'ID du projet depuis l'URL
        elif request.method == 'DELETE':
            # Assurez-vous que 'contributor_id' est le nom correct de votre paramètre dans l'URL
            contributor_id = view.kwargs.get('pk')
            if contributor_id:
                contributor = get_object_or_404(Contributor, pk=contributor_id)
                project = contributor.project
                return project.author == request.user

        return False
