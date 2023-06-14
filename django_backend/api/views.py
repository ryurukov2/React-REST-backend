# from time import sleep
# from django.http import JsonResponse
# from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response

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
    serializer_class_ProjectTasks = TaskSerializer
    serializer_class_Project = ProjectSerializer
    # queryset = ProjectTasks.objects.filter(id=last_project.id)
    def get_queryset_ProjectTasks(self):
        last_task = ProjectTasks.get_most_recent_task()
        print(last_task.project)
        return ProjectTasks.objects.filter(project=last_task.project).order_by('-last_update_on')
    def get_queryset_Project(self, id):
        # last_project = Project.get_most_recent_project()
        # print(last_project.id)
        return Project.objects.get(id=id)


    def list(self, request, *args, **kwargs):
        tasks = self.serializer_class_ProjectTasks(self.get_queryset_ProjectTasks(), many=True)
        project = self.serializer_class_Project(self.get_queryset_Project(tasks.data[0]['project']), many=False)
        print(tasks.data[0]['project'])
        return Response({"project": project.data,
                         "tasks": tasks.data})
    