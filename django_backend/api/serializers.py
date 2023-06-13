from rest_framework import serializers

from .models import Project, ProjectTasks


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('id', 'name', 'description', 'last_update_on', 'created_on')


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectTasks
        fields = ('id', 'project', 'priority', 'description', 'completion_status', 'last_update_on', 'created_on')