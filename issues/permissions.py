
from rest_framework.permissions import BasePermission, SAFE_METHODS
from projects.models import Project  # Assurez-vous d'importer le modèle Project
from contributors.models import Contributor  # Importez votre modèle Contributor


class IsContributor(BasePermission):
    message = "Seuls les contributeurs du projet peuvent effectuer cette action."

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        project_id = request.data.get('project')
        if project_id:
            project = Project.objects.filter(id=project_id).first()
            if project:
                # Vérifiez si l'utilisateur est un contributeur ou l'auteur du projet
                return Contributor.objects.filter(project=project, user=request.user).exists()
            return False  # Si le projet n'existe pas, refusez l'accès


class IsAuthor(BasePermission):
    message = "Seul l'auteur peut modifier ou supprimer cet objet."

    def has_object_permission(self, request, view, obj):
        message = "Seul l'auteur peut modifier ou supprimer cet objet."

        if not request.user or not request.user.is_authenticated:
            return False

        return obj.author == request.user
