from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

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