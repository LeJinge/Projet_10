from django.db.models import Q
from rest_framework import viewsets, permissions
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
        Ce queryset retourne tous les contributeurs pour lesquels l'utilisateur actuel est l'auteur du projet ou un administrateur du projet.
        """
        user = self.request.user
        if user.is_authenticated:
            # Filtrer les contributeurs où l'utilisateur est l'auteur du projet
            # ou un administrateur dans l'un des projets.
            return Contributor.objects.filter(
                Q(project__author=user) |
                Q(project__contributor__user=user, project__contributor__role='Administrator')
            ).distinct()
        return Contributor.objects.none()
