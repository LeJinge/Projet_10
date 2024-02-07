from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

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
        serializer.save(author=self.request.user)

    @action(detail=False, methods=['put', 'patch'], url_path='update-comment')
    def update_comment(self, request, *args, **kwargs):
        comment_id = request.data.get('id')
        if not comment_id:
            return Response({"error": "ID du Commentaire manquant"}, status=status.HTTP_400_BAD_REQUEST)

        comment = get_object_or_404(Comment, pk=comment_id)
        serializer = self.get_serializer(comment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['delete'], url_path='delete-comment')
    def delete_comment(self, request, *args, **kwargs):
        comment_id = request.data.get('id')
        if not comment_id:
            return Response({"error": "ID du Commentaire manquant"}, status=status.HTTP_400_BAD_REQUEST)

        comment = get_object_or_404(Comment, pk=comment_id)
        self.perform_destroy(comment)
        return Response(status=status.HTTP_204_NO_CONTENT)



