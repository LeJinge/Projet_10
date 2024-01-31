from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

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

    @action(detail=False, methods=['put', 'patch'], url_path='update-issue')
    def update_issue(self, request, *args, **kwargs):
        issue_id = request.data.get('id')
        if not issue_id:
            return Response({"error": "ID de l'Issue manquant"}, status=status.HTTP_400_BAD_REQUEST)

        issue = get_object_or_404(Issue, pk=issue_id)
        serializer = self.get_serializer(issue, data=request.data, partial=True)
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['delete'], url_path='delete-issue')
    def delete_issue(self, request, *args, **kwargs):
        issue_id = request.data.get('id')
        if not issue_id:
            return Response({"error": "ID de l'Issue manquant"}, status=status.HTTP_400_BAD_REQUEST)

        issue = get_object_or_404(Issue, pk=issue_id)
        self.perform_destroy(issue)
        return Response(status=status.HTTP_204_NO_CONTENT)