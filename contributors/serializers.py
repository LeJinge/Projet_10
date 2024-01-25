from rest_framework import serializers
from .models import Contributor
from users.models import CustomUser
from projects.models import Project


class ContributorSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field='username',
        queryset=CustomUser.objects.all()
    )
    project = serializers.SlugRelatedField(
        slug_field='title',
        queryset=Project.objects.all()
    )

    class Meta:
        model = Contributor
        fields = ['id', 'user', 'project', 'role']

    def validate(self, data):
        # Exemple de validation personnalisée
        if Contributor.objects.filter(user=data['user'], project=data['project']).exists():
            raise serializers.ValidationError("Cet utilisateur est déjà contributeur de ce projet.")
        return data
