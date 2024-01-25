from rest_framework.permissions import BasePermission


class IsProjectAuthor(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Vérifie si l'utilisateur est l'auteur du projet
        return obj.author == request.user


class IsProjectAdministrator(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Vérifie si l'utilisateur est un administrateur du projet
        return obj.contributors.filter(user=request.user, role='Administrator').exists()


class IsProjectEditor(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Vérifie si l'utilisateur est un éditeur du projet
        return obj.contributors.filter(user=request.user, role='Editor').exists()


class IsProjectViewer(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Vérifie si l'utilisateur est un spectateur du projet
        return obj.contributors.filter(user=request.user, role='Viewer').exists()


class IsAssignee(BasePermission):
    """ Autorise l'assignee à effectuer certaines actions sur l'issue. """

    def has_object_permission(self, request, view, obj):
        # Vérifie si l'utilisateur est l'assignee de l'issue
        return obj.assignee == request.user


