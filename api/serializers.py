from rest_framework import serializers

from todo.models import Todo


class TodoSerializer(serializers.ModelSerializer):
    # cannot be populated by user
    created = serializers.ReadOnlyField()
    datecompleted = serializers.ReadOnlyField()
    # to hide user field from create form
    user = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = Todo
        fields = ['id', 'title', 'memo', 'created', 'datecompleted', 'important', 'user']
