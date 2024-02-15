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

    def perform_create(self, serializer):
        # Sauvegarde du contributeur avec le projet actuel
        project_id = self.kwargs.get('project_id')
        project = Project.objects.get(pk=project_id)
        serializer.save(project=project)
