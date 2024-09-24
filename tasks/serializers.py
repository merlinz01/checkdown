from .models import Task, Status, User
from rest_framework import serializers


class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = [
            "pk",
            "name",
            "description",
            "status",
            "assignee",
            "due_date",
            "priority",
            "parent",
            "created",
            "updated",
        ]


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = [
            "pk",
            "name",
            "description",
            "order",
            "color",
            "closed",
            "created",
            "updated",
        ]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "pk",
            "username",
            "email",
            "first_name",
            "last_name",
        ]
