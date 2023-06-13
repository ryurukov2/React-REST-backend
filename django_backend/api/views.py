from time import sleep
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import generics

from .models import Project, ProjectTasks
from .serializers import ProjectSerializer, TaskSerializer
# Create your views here.


class CreateProjectsView(generics.CreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class ListProjectsView(generics.ListAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    # def get(self, request, *args, **kwargs):
    #     return super().get(request, *args, **kwargs)


class ProjectDeleteView(generics.DestroyAPIView):
    # queryset = Project.objects.all()
    
    serializer_class = ProjectSerializer
    def get_queryset(self):
        project_id=self.kwargs['pk']
        return Project.objects.filter(id=project_id)

class ProjectDetailView(generics.RetrieveAPIView):
    # queryset = Project.objects.all()

    serializer_class = ProjectSerializer

    def get_queryset(self):
        task_id=self.kwargs['pk']
        return Project.objects.filter(id=task_id)

class TasksListView(generics.ListAPIView):
    serializer_class = TaskSerializer
    pagination_class = None

    def get_queryset(self):
        project_id = self.kwargs['project_id']
        return ProjectTasks.objects.filter(project__id=project_id)
    
    
class TasksCreateView(generics.CreateAPIView):
    # queryset = ProjectTasks.objects.all()
    serializer_class = TaskSerializer

class TasksEditView(generics.UpdateAPIView):
    # queryset = ProjectTasks.objects.all()
    
    serializer_class = TaskSerializer
    def get_queryset(self):
        task_id=self.kwargs['pk']
        return ProjectTasks.objects.filter(id=task_id)


class TasksDeleteView(generics.DestroyAPIView):
    serializer_class = TaskSerializer
    def get_queryset(self):
        task_id=self.kwargs['pk']
        return ProjectTasks.objects.filter(id=task_id)
    

class TaskGetLastEditedView(generics.ListAPIView):
    serializer_class = TaskSerializer
    
    # queryset = ProjectTasks.objects.filter(id=last_project.id)
    def get_queryset(self):
        last_project = ProjectTasks.get_most_recent_task()
        print(last_project.project)
        return ProjectTasks.objects.filter(project=last_project.project).order_by('-last_update_on')

    