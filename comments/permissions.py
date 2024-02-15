
from rest_framework.permissions import BasePermission


from contributors.models import Contributor
from issues.models import Issue


class IsContributor(BasePermission):
    message = "Vous devez être un contributeur du projet pour effectuer cette action."

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        issue_id = request.data.get('issue')

        if issue_id:
            try:
                issue = Issue.objects.get(pk=issue_id)
                project = issue.project
                # Vérifier si l'utilisateur est un contributeur du projet lié à l'issue
                return Contributor.objects.filter(user=request.user, project=project).exists()
            except Issue.DoesNotExist:
                # Si l'issue n'existe pas, la permission est refusée
                return False
        # Si l'ID de l'issue n'est pas fourni, la permission est également refusée
        return False


class IsAuthor(BasePermission):
    message = "Seul l'auteur peut modifier ou supprimer cet objet."

    def has_object_permission(self, request, view, obj):
        if not request.user or not request.user.is_authenticated:
            return False
        return obj.author == request.user
