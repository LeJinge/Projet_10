from django.db.models import Q
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Comment
from .permissions import IsAuthor, IsContributor
from .serializers import CommentSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_permissions(self):
        if self.action in ['create']:
            permission_classes = [IsContributor]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthor]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            # Pour les actions de lecture, filtrer les commentaires soit par auteur, soit par appartenance au projet
            # via l'issue
            if self.action in ['list', 'retrieve']:
                return Comment.objects.filter(
                    Q(author=user) |
                    Q(issue__project__contributors=user)
                ).distinct()
            else:
                return super().get_queryset()
        return Comment.objects.none()

