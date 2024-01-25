from rest_framework import serializers
from .models import Project
from contributors.serializers import ContributorSerializer  # Importer le sérialiseur Contributor


class ProjectSerializer(serializers.ModelSerializer):
    contributors = ContributorSerializer(many=True, read_only=True, required=False)

    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'type', 'author', 'contributors', 'creation_date', 'last_update']
