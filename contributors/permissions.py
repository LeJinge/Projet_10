from rest_framework.permissions import BasePermission
from contributors.models import Contributor
from projects.models import Project
from issues.models import Issue


class IsProjectAuthor(BasePermission):
    """
    Autorise seulement l'auteur du projet à effectuer certaines actions.
    """
    def has_permission(self, request, view):
        # Vérifie si l'utilisateur est l'auteur du projet
        return Project.objects.filter(id=view.kwargs['project_id'], author=request.user).exists()


class IsProjectAdministrator(BasePermission):
    """
    Autorise seulement les administrateurs du projet à effectuer certaines actions.
    """

    def has_object_permission(self, request, view, obj):
        print(request.user)
        # Vérifie si l'utilisateur est un administrateur du projet
        if hasattr(request.user, 'is_contributor') and 'project_id' in obj.project_id:
            return (
                request.user.is_contributor.role == 'Administrator' and
                request.user.is_contributor.project_id == obj.project_id
            )
        return False


class IsProjectEditor(BasePermission):
    """
    Autorise seulement les éditeurs du projet à effectuer certaines actions.
    """
    def has_object_permission(self, request, view, obj):
        return Contributor.objects.filter(project_id=view.kwargs['project_id'], user=request.user, role='Editor').exists()


class IsProjectViewer(BasePermission):
    """
    Autorise seulement les visualisateurs du projet à effectuer certaines actions.
    """
    def has_object_permission(self, request, view, obj):
        return Contributor.objects.filter(project_id=view.kwargs['project_id'], user=request.user,
                                          role='Viewer').exists()


class IsAssignee(BasePermission):
    """
    Autorise seulement l'assigné d'une tâche à effectuer certaines actions.
    """
    def has_object_permission(self, request, view, obj):
        return obj.assignees == request.user if isinstance(obj, Issue) else False


