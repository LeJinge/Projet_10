from django.db.models import Q
from rest_framework import viewsets
from .models import Issue
from .permissions import IsAuthor, IsContributor
from rest_framework.permissions import IsAuthenticated

from .serializers import IssueSerializer


class IssueViewSet(viewsets.ModelViewSet):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action in ['create']:
            permission_classes = [IsAuthenticated, IsContributor]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated, IsAuthor]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            # Pour les actions de lecture, filtrer les commentaires soit par auteur, soit par appartenance au projet
            # via l'issue
            if self.action in ['list', 'retrieve']:
                return Issue.objects.filter(
                    Q(author=user) |
                    Q(project__contributors=self.request.user)
                ).distinct()
            else:
                return super().get_queryset()
        return Issue.objects.none()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
