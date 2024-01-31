from rest_framework.permissions import BasePermission

from contributors.models import Contributor
from projects.models import Project


class IsProjectAuthor(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Vérifie si l'utilisateur est l'auteur du projet
        return obj.project.author == request.user


class IsProjectAdministrator(BasePermission):
    class IsProjectAdministrator(BasePermission):
        def has_object_permission(self, request, view, obj):
            return Contributor.objects.filter(user=request.user, project=obj, role='Administrator').exists()


class IsProjectEditor(BasePermission):
    class IsProjectAdministrator(BasePermission):
        def has_object_permission(self, request, view, obj):
            return Contributor.objects.filter(user=request.user, project=obj, role='Editor').exists()


class IsProjectViewer(BasePermission):
    class IsProjectAdministrator(BasePermission):
        def has_object_permission(self, request, view, obj):
            return Contributor.objects.filter(user=request.user, project=obj, role='Viewer').exists()


class IsAssignee(BasePermission):
    """ Autorise l'assignee à effectuer certaines actions sur l'issue. """

    def has_object_permission(self, request, view, obj):
        # Vérifie si l'utilisateur est l'assignee de l'issue
        return obj.assignee == request.user


class IsProjectContributor(BasePermission):
    """ Autorise les contributeurs du projet à effectuer certaines actions. """

    def has_object_permission(self, request, view, obj):
        # Vérifie si l'utilisateur est un contributeur du projet associé au commentaire
        return obj.project.contributors.filter(user=request.user).exists()


