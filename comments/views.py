from django.core.exceptions import PermissionDenied
from rest_framework import viewsets, permissions

from comments.models import Comment
from comments.serializers import CommentSerializer
from contributors.permissions import IsProjectAdministrator, IsAssignee


# Create your views here.
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_permissions(self):
        """
        Retourne les permissions personnalisées en fonction de l'action.
        """
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAuthenticated, IsProjectAdministrator | IsAssignee]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        # Sauvegarde du projet avec l'utilisateur actuel comme auteur
        serializer.save(author=self.request.user)
