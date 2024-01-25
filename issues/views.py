from rest_framework import viewsets, permissions
from .models import Issue
from .serializers import IssueSerializer
from contributors.permissions import IsProjectAdministrator, IsAssignee
from rest_framework.exceptions import PermissionDenied


class IssueViewSet(viewsets.ModelViewSet):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer

    def get_permissions(self):
        """
        Retourne les permissions personnalisées en fonction de l'action.
        """
        if self.action in ['create', 'destroy']:
            permission_classes = [IsProjectAdministrator]
        elif self.action in ['update', 'partial_update']:
            permission_classes = [IsProjectAdministrator | IsAssignee]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    def perform_update(self, serializer):
        issue = serializer.instance
        user = self.request.user

        # Si l'utilisateur est l'assignee, autoriser uniquement la modification du statut
        if issue.assignee == user:
            if list(self.request.data.keys()) != ['status']:
                raise PermissionDenied("Vous ne pouvez modifier que le statut de l'issue.")

        # Pour les administrateurs, aucune restriction supplémentaire
        serializer.save()
