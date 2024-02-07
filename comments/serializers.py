from rest_framework import serializers
from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"
        read_only_fields = ['id', 'author', 'creation_date', 'last_update']

    def __init__(self, *args, **kwargs):
        super(CommentSerializer, self).__init__(*args, **kwargs)
        # Lors de la mise à jour, rendre le champ `issue` en lecture seule
        if self.instance is not None:
            self.fields['issue'].read_only = True
