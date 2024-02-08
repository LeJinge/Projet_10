from django.db.models import Q
from rest_framework import viewsets, permissions

from comments.models import Comment
from comments.serializers import CommentSerializer
from contributors.permissions import IsProjectAdministrator, IsAssignee


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

    def get_queryset(self):
        """
        Ce queryset retourne les commentaires pour lesquels l'utilisateur actuel est assigné à l'issue
        correspondante ou est un administrateur du projet associé à l'issue.
        """
        user = self.request.user
        if user.is_authenticated:
            return Comment.objects.filter(
                Q(issue__assignees=user) |
                Q(issue__project__contributors__user=user, issue__project__contributors__role='Administrator')
            ).distinct()
        return Comment.objects.none()

    def perform_create(self, serializer):
        """
        Assigner l'utilisateur actuel comme auteur du commentaire lors de la création.
        """
        serializer.save(author=self.request.user)
