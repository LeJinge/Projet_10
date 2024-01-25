from rest_framework import viewsets, permissions

from contributors.models import Contributor
from contributors.permissions import IsProjectAdministrator, IsProjectViewer, IsProjectAuthor
from projects.models import Project
from projects.serializers import ProjectSerializer


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
            permission_classes = [permissions.IsAuthenticated, IsProjectViewer]
        elif self.action in ['update', 'partial_update']:
            permission_classes = [IsProjectAdministrator]
        elif self.action == 'destroy':
            permission_classes = [IsProjectAuthor]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        # Sauvegarde du projet avec l'utilisateur actuel comme auteur
        project = serializer.save(author=self.request.user)
        # Création d'un enregistrement Contributor pour associer l'utilisateur au projet en tant qu'Administrator
        Contributor.objects.create(user=self.request.user, project=project, role='Administrator')
