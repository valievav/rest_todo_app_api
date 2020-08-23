from rest_framework import serializers

from todo.models import Todo


class TodoSerializer(serializers.ModelSerializer):
    created = serializers.ReadOnlyField()  # cannot be populated by user
    datecompleted = serializers.ReadOnlyField()
    user = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())  # to hide user field from create form

    class Meta:
        model = Todo
        fields = ['id', 'title', 'memo', 'created', 'datecompleted', 'important', 'user']


class TodoCompleteSerializer(serializers.ModelSerializer):  # separate serializer - user can't update any field for complete api call (datecompleted is auto set)
    class Meta:
        model = Todo
        fields = ['id']
        read_only_fields = ['title', 'memo', 'created', 'datecompleted', 'important', 'user']
