from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from projects.models import Project
from .models import Contributor
from .permissions import IsProjectAuthor
from .serializers import ContributorSerializer


class ContributorViewSet(viewsets.ModelViewSet):
    queryset = Contributor.objects.all()
    serializer_class = ContributorSerializer
    permission_classes = [IsAuthenticated, IsProjectAuthor]

    def get_permissions(self):
        if self.action in ['create', 'destroy']:
            permission_classes = [IsProjectAuthor]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        # Sauvegarde du contributeur avec le projet actuel
        project_id = self.request.data.get('project')
        project = get_object_or_404(Project, pk=project_id)
        serializer.save(project=project)

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            if self.action in ['list', 'retrieve']:
                return Contributor.objects.filter(
                    Q(project__author=user)
                ).distinct()
            else:
                return super().get_queryset()
        return Contributor.objects.none()


