from rest_framework import viewsets, permissions, status
from rest_framework.exceptions import PermissionDenied, ValidationError
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

    def perform_create(self, serializer):
        role = self.request.data.get('role')
        valid_roles = [choice[0] for choice in Contributor.ROLE_CHOICES]
        if role not in valid_roles:
            raise ValidationError("Rôle invalide.")
        serializer.save(role=role)

    def perform_update(self, serializer):
        # Même logique que dans perform_create si nécessaire
        serializer.save()
