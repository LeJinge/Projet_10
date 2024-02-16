from django.db.models import Q
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from contributors.models import Contributor
from .models import Project
from .permissions import IsAuthor
from .serializers import ProjectSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated, IsAuthor]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        """
        Ce queryset est conçu pour retourner les projets que l'utilisateur a le droit de voir,
        incluant les projets où l'utilisateur est l'auteur ou un contributeur.
        """
        user = self.request.user
        if user.is_authenticated:
            # Pour les actions de lecture, filtrer les commentaires soit par auteur, soit par appartenance au projet
            # via l'issue
            if self.action in ['list', 'retrieve']:
                return Project.objects.filter(
                    Q(author=user) |
                    Q(contributors=user)
                ).distinct()
            else:
                return super().get_queryset()
        return Project.objects.none()

    def perform_create(self, serializer):
        """
        Sauvegarde du projet avec l'utilisateur actuel comme auteur.
        L'auteur est également ajouté en tant que contributeur du projet.
        """
        project = serializer.save(author=self.request.user)
        Contributor.objects.create(user=self.request.user, project=project)
