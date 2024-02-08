from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

from users.models import CustomUser
from .models import Issue
from .serializers import IssueSerializer
from contributors.permissions import IsProjectAdministrator, IsAssignee


class IssueViewSet(viewsets.ModelViewSet):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer

    def get_permissions(self):
        if self.action in ['create', 'destroy']:
            permission_classes = [IsProjectAdministrator]
        elif self.action in ['update', 'partial_update']:
            permission_classes = [IsProjectAdministrator | IsAssignee]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Issue.objects.filter(
                Q(assignees=user) |
                Q(project__contributors=user, project__contributors__role='Administrator')
            ).distinct()
        return Issue.objects.none()

    def perform_create(self, serializer):
        """
        Définit automatiquement l'utilisateur connecté comme auteur de l'issue lors de la création.
        """
        serializer.save(author=self.request.user)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        # Assurez-vous que l'utilisateur a la permission de supprimer cette issue
        if not self.check_object_permissions(request, instance):
            raise PermissionDenied("Vous n'êtes pas autorisé à supprimer cette issue.")

    @action(detail=True, methods=['post', 'delete'], url_path='manage-assignees')
    def manage_assignees(self, request, *args, **kwargs):
        instance = self.get_object()

        user_id = request.data.get('user_id')
        if not user_id:
            return Response({"error": "ID de l'utilisateur manquant"}, status=status.HTTP_400_BAD_REQUEST)

        user = get_object_or_404(CustomUser, pk=user_id)

        if request.method == 'POST':
            instance.assignees.add(user)
            message = "Utilisateur ajouté aux assignés avec succès."
        elif request.method == 'DELETE':
            instance.assignees.remove(user)
            message = "Utilisateur supprimé des assignés avec succès."

        instance.save()

        return Response({"message": message}, status=status.HTTP_200_OK)
