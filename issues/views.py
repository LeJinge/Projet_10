from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from users.models import CustomUser
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

    @action(detail=False, methods=['post', 'delete'], url_path='manage-assignees')
    def manage_assignees(self, request, *args, **kwargs):
        """
        Ajoute ou supprime des utilisateurs de la liste des assignees.
        Utilise la méthode POST pour ajouter, DELETE pour supprimer.
        Les données de requête doivent inclure 'issue_id' et 'user_id'.
        """
        issue_id = request.data.get('issue_id')
        user_id = request.data.get('user_id')

        if not issue_id or not user_id:
            return Response({"error": "ID de l'issue ou de l'utilisateur manquant"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            issue = Issue.objects.get(pk=issue_id)
        except Issue.DoesNotExist:
            return Response({"error": "Issue non trouvée"}, status=status.HTTP_404_NOT_FOUND)

        try:
            user = CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            return Response({"error": "Utilisateur non trouvé"}, status=status.HTTP_404_NOT_FOUND)

        if request.method == 'POST':
            # Ajoute l'utilisateur aux assignees de l'issue
            issue.assignees.add(user)
            return Response({"message": "Utilisateur ajouté aux assignees"}, status=status.HTTP_200_OK)

        elif request.method == 'DELETE':
            # Supprime l'utilisateur des assignees de l'issue
            if user in issue.assignees.all():
                issue.assignees.remove(user)
                return Response({"message": "Utilisateur supprimé des assignees"}, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({"error": "L'utilisateur n'est pas un assignee de cette issue"},
                                status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response({"error": "Méthode non autorisée"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
