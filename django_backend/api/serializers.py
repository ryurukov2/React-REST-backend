from rest_framework import serializers

from .models import Project, ProjectTasks
from django.contrib.auth.models import User 


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('id', 'name', 'description', 'last_update_on', 'created_on', 'owner', 'assigned')
        read_only_fields = ('owner',)

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectTasks
        fields = ('id', 'project', 'priority', 'description', 'completion_status', 'last_update_on', 'created_on')

class AddAssigneeSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()


class AssigneeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')