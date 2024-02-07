from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from projects.models import Project
from .models import Contributor
from .permissions import IsProjectAuthor
from .serializers import ContributorSerializer


class ContributorViewSet(viewsets.ModelViewSet):
    queryset = Contributor.objects.all()
    serializer_class = ContributorSerializer

    def get_permissions(self):
        """
        Instance et retourne la liste des permissions que cette vue requiert.
        """
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAuthenticated, IsProjectAuthor]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        """
        Ce queryset filtre les contributeurs par l'ID du projet passé en paramètre de requête.
        """
        project_id = self.request.query_params.get('project_id')
        if project_id is not None:
            project = get_object_or_404(Project, pk=project_id)
            # Ici, ajoutez votre logique de permission pour s'assurer que l'utilisateur est autorisé
            if not IsProjectAuthor().has_object_permission(self.request, self, project):
                self.permission_denied(
                    self.request,
                    message="Vous n'avez pas la permission de voir les contributeurs de ce projet."
                )
            return self.queryset.filter(project=project)
        return self.queryset.none()  # Retourner un queryset vide si l'ID du projet n'est pas fourni

    @action(detail=False, methods=['put', 'patch'], url_path='update-contributor')
    def update_contributor(self, request, *args, **kwargs):
        contributor_id = request.data.get('id')
        if not contributor_id:
            return Response({"error": "ID du Contributor manquant"}, status=status.HTTP_400_BAD_REQUEST)

        contributor = get_object_or_404(Contributor, pk=contributor_id)
        serializer = self.get_serializer(contributor, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['delete'], url_path='delete-contributor')
    def delete_contributor(self, request, *args, **kwargs):
        contributor_id = request.data.get('id')
        if not contributor_id:
            return Response({"error": "ID du Contributor manquant"}, status=status.HTTP_400_BAD_REQUEST)

        contributor = get_object_or_404(Contributor, pk=contributor_id)
        self.perform_destroy(contributor)
        return Response(status=status.HTTP_204_NO_CONTENT)