from rest_framework import serializers
from .models import Issue
from users.models import CustomUser
from projects.serializers import ProjectSerializer
from users.serializers import CustomUserSerializer


class IssueSerializer(serializers.ModelSerializer):
    project = ProjectSerializer(read_only=True)
    author = CustomUserSerializer(read_only=True)
    assignee = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.filter(contributor__role='Editor'),
        required=False,
        allow_null=True
    )

    class Meta:
        model = Issue
        fields = [
            'id',
            'title',
            'description',
            'creation_date',
            'last_update',
            'project',
            'status',
            'priority',
            'author',
            'assignee',
        ]
