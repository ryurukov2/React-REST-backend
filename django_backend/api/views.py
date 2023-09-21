from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Project, ProjectTasks
from .serializers import AssigneeSerializer, AddAssigneeSerializer, ProjectSerializer, TaskSerializer
from rest_framework.authentication import TokenAuthentication
from .permissions import IsProjectOwner, IsProjectOwnerOrAssigned
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import User
from django.db.models import Q


class CreateProjectsView(generics.CreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ListProjectsView(generics.ListAPIView):
    serializer_class = ProjectSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        r = Project.objects.filter(Q(owner=user.id)| Q(assigned=user.id)).distinct()
        return r


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
        
class AddAssigneeView(generics.UpdateAPIView):
    queryset = Project.objects.all()
    serializer_class = AddAssigneeSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsProjectOwnerOrAssigned]

    def update(self, request, *args, **kwargs):
        project = self.get_object()
        print(request.data['username'])
        assigneeUsername = request.data['username']
        try:
            user_to_assign = User.objects.get(username=assigneeUsername)
        except User.DoesNotExist:
            return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        project.assigned.add(user_to_assign)
        project.save()

        return Response({"detail": "Assignee added successfully!"}, status=status.HTTP_200_OK)
    
class RetrieveProjectOwnerView(generics.RetrieveAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsProjectOwnerOrAssigned]
    # queryset = User.objects.all()
    

    def get_queryset(self):
        project_id = self.kwargs.get('pk')
        project = Project.objects.filter(id=project_id)
        return project

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        return Response({"owner": instance.owner.username, "status": 200}, status=status.HTTP_200_OK)   

class ListProjectAssigned(generics.ListAPIView):
    serializer_class = AssigneeSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsProjectOwnerOrAssigned]
    

    def get_queryset(self):
        project_id = self.kwargs.get('pk')
        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            return User.objects.none()
        
        return project.assigned.all()
