from rest_framework.permissions import BasePermission
from contributors.models import Contributor
from projects.models import Project


class IsProjectAuthor(BasePermission):
    """
    Autorise seulement l'auteur du projet à effectuer certaines actions.
    """
    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Project):
            return obj.author == request.user
        return obj.project.author == request.user


class IsProjectAdministrator(BasePermission):
    """
    Autorise seulement les administrateurs du projet à effectuer certaines actions.
    """
    def has_object_permission(self, request, view, obj):
        return Contributor.objects.filter(user=request.user, project=obj, role='Administrator').exists()


class IsProjectEditor(BasePermission):
    """
    Autorise seulement les éditeurs du projet à effectuer certaines actions.
    """
    def has_object_permission(self, request, view, obj):
        return Contributor.objects.filter(user=request.user, project=obj, role='Editor').exists()


class IsProjectViewer(BasePermission):
    """
    Autorise seulement les visualisateurs du projet à effectuer certaines actions.
    """
    def has_object_permission(self, request, view, obj):
        return Contributor.objects.filter(user=request.user, project=obj, role='Viewer').exists()


class IsAssignee(BasePermission):
    """
    Autorise seulement l'assigné d'une tâche à effectuer certaines actions.
    """
    def has_object_permission(self, request, view, obj):
        return obj.assignee == request.user


class IsProjectContributor(BasePermission):
    """
    Autorise tous les contributeurs du projet à effectuer certaines actions.
    """
    def has_object_permission(self, request, view, obj):
        project = obj if isinstance(obj, Project) else obj.project
        return project.contributors.filter(id=request.user.id).exists()
