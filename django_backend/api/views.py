from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Project, ProjectTasks
from .serializers import ProjectSerializer, TaskSerializer
from rest_framework.authentication import TokenAuthentication
from .permissions import IsProjectOwner, IsProjectOwnerOrAssigned
from django.core.exceptions import PermissionDenied


class CreateProjectsView(generics.CreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ListProjectsView(generics.ListAPIView):
    # queryset = Project.objects.filter(created_by=)
    # queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Project.objects.filter(owner=user.id)


class ProjectDeleteView(generics.DestroyAPIView):

    serializer_class = ProjectSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsProjectOwner]

    def get_queryset(self):
        project_id = self.kwargs['pk']
        return Project.objects.filter(id=project_id)


class ProjectDetailView(generics.RetrieveAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsProjectOwnerOrAssigned]

    serializer_class = ProjectSerializer

    def get_queryset(self):
        task_id = self.kwargs['pk']
        return Project.objects.filter(id=task_id)


class TasksListView(generics.ListAPIView):
    serializer_class = TaskSerializer
    pagination_class = None
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        project_id = self.kwargs.get('project_id')
        project = get_object_or_404(Project, id=project_id)

        has_perm = (
            project.owner == self.request.user or self.request.user in project.assigned.all())
        if not has_perm:
            raise PermissionDenied(
                "You don't have permission to view this project's tasks.")

        return ProjectTasks.objects.filter(project=project)


class TasksCreateView(generics.CreateAPIView):
    serializer_class = TaskSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


class TasksEditView(generics.UpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsProjectOwnerOrAssigned]
    serializer_class = TaskSerializer

    def get_queryset(self):
        task_id = self.kwargs['pk']
        return ProjectTasks.objects.filter(id=task_id)


class TasksDeleteView(generics.DestroyAPIView):
    serializer_class = TaskSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsProjectOwner]
    def get_queryset(self):
        task_id = self.kwargs['pk']
        return ProjectTasks.objects.filter(id=task_id)


class TaskGetLastEditedView(generics.ListAPIView):
    serializer_class_ProjectTasks = TaskSerializer
    serializer_class_Project = ProjectSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset_Project(self):
        last_project = Project.get_most_recent_project(self.request.user.id)
        return last_project
    
    def get_queryset_ProjectTasks(self, project_id):
        return ProjectTasks.objects.filter(project=project_id).order_by('-last_update_on')



    def list(self, request, *args, **kwargs):
        last_project = self.get_queryset_Project()
        if(last_project):
            project = self.serializer_class_Project(
                last_project, many=False)
            tasks = self.serializer_class_ProjectTasks(
                self.get_queryset_ProjectTasks(last_project.id), many=True)
        
            return Response({"project": project.data,
                            "tasks": tasks.data})
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)