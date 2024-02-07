from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q

from projects.models import Project
from projects.serializers import ProjectSerializer
from contributors.models import Contributor
from contributors.permissions import IsProjectAdministrator, IsProjectAuthor, IsProjectContributor


class ProjectViewSet(viewsets.ModelViewSet):
    """
    Un viewset pour voir et éditer les instances de projets.
    """
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()

    def get_permissions(self):
        """
        Instance et retourne la liste des permissions que cette vue requiert, selon l'action.
        """
        if self.action == 'create':
            permission_classes = [permissions.IsAuthenticated]
        elif self.action in ['retrieve', 'list']:
            permission_classes = [permissions.IsAuthenticated, IsProjectContributor]
        elif self.action in ['update', 'partial_update']:
            permission_classes = [permissions.IsAuthenticated, IsProjectAdministrator]
        elif self.action == 'destroy':
            permission_classes = [permissions.IsAuthenticated, IsProjectAuthor]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        """
        Ce queryset est conçu pour retourner les projets que l'utilisateur a le droit de voir.
        """
        user = self.request.user
        if user.is_authenticated:
            return Project.objects.filter(
                Q(author=user) |
                Q(contributors=user.id)
            ).distinct()
        return Project.objects.none()

    def perform_create(self, serializer):
        """
        Sauvegarde du projet avec l'utilisateur actuel comme auteur et l'ajoute comme administrateur du projet.
        """
        project = serializer.save(author=self.request.user)
        Contributor.objects.create(user=self.request.user, project=project, role='Administrator')

    @action(detail=True, methods=['put', 'patch'], url_path='update-project')
    def update_project(self, request, *args, **kwargs):
        project = self.get_object()
        serializer = self.get_serializer(project, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['delete'], url_path='delete-project')
    def delete_project(self, request, *args, **kwargs):
        project = self.get_object()
        self.perform_destroy(project)
        return Response(status=status.HTTP_204_NO_CONTENT)
