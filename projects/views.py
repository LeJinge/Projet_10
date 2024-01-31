from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from projects.models import Project
from projects.serializers import ProjectSerializer
from contributors.models import Contributor
from contributors.permissions import IsProjectAdministrator, IsProjectAuthor, IsProjectContributor


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def get_permissions(self):
        """
        Instance et retourne la liste des permissions que cette vue requiert.
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

    def perform_create(self, serializer):
        # Sauvegarde du projet avec l'utilisateur actuel comme auteur
        project = serializer.save(author=self.request.user)
        # Création d'un enregistrement Contributor pour associer l'utilisateur au projet en tant qu'Administrator
        Contributor.objects.create(user=self.request.user, project=project, role='Administrator')

    @action(detail=False, methods=['put', 'patch'], url_path='update-project')
    def update_project(self, request, *args, **kwargs):
        project_id = request.data.get('id')
        if not project_id:
            return Response({"error": "ID du projet manquant"}, status=status.HTTP_400_BAD_REQUEST)

        project = get_object_or_404(Project, pk=project_id)
        serializer = self.get_serializer(project, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['delete'], url_path='delete-project')
    def delete_project(self, request, *args, **kwargs):
        project_id = request.data.get('id')
        if not project_id:
            return Response({"error": "ID du projet manquant"}, status=status.HTTP_400_BAD_REQUEST)

        project = get_object_or_404(Project, pk=project_id)
        self.perform_destroy(project)
        return Response(status=status.HTTP_204_NO_CONTENT)
