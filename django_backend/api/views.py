from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Project, ProjectTasks
from .serializers import AssigneeSerializer, AddAssigneeSerializer, CompletionStatusCountSerializer, PriorityCountSerializer, ProjectSerializer, TaskSerializer
from rest_framework.authentication import TokenAuthentication
from .permissions import IsProjectOwner, IsProjectOwnerOrAssigned
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework.views import APIView
from django.db.models import Count


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
        r = Project.objects.filter(
            Q(owner=user.id) | Q(assigned=user.id)).distinct()
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
        if (last_project):
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


class DashboardView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        username = request.user.username
        owner_of = Project.objects.filter(owner=request.user).count()
        assigned_to = Project.objects.filter(assigned=request.user).count()
        non_resolved_tasks = ProjectTasks.objects.filter((Q(project__assigned=request.user) | Q(
            project__owner=request.user)) & ~Q(completion_status='RESOLVED')).count()
        resolved_tasks = ProjectTasks.objects.filter((Q(project__assigned=request.user) | Q(
            project__owner=request.user)) & Q(completion_status='RESOLVED')).count()
        todo_tasks = ProjectTasks.objects.filter((Q(project__assigned=request.user) | Q(
            project__owner=request.user)) & Q(completion_status='TODO')).count()

        print(username)

        data = {
            'username': username,
            'owner_of': owner_of,
            'assigned_to': assigned_to,
            'non_resolved_tasks': non_resolved_tasks,
            'resolved_tasks': resolved_tasks,
            'todo_tasks': todo_tasks
        }
        return Response(data, status=status.HTTP_200_OK)

# average number of tasks per project
# average priority of tasks
# number of "completed" projects (if all tasks are with status RESOLVED)
#


class AnalyticsView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        # print(request.user)
        # pending_tasks = ProjectTasks.objects.filter((Q(project__assigned=request.user)|Q(project__owner=request.user))&~Q(completion_status='RESOLVED')).count()
        # resolved_tasks = ProjectTasks.objects.filter((Q(project__assigned=request.user)|Q(project__owner=request.user))&Q(completion_status='RESOLVED')).count()

        queryset = ProjectTasks.objects.filter(
            Q(project__owner=request.user) | Q(project__assigned=request.user))

        completion_status_counts = queryset.values(
            'completion_status').annotate(count=Count('completion_status'))

        priority_counts = queryset.values(
            'priority').annotate(count=Count('priority'))

        completion_serializer = CompletionStatusCountSerializer(
            completion_status_counts, many=True)
        priority_serializer = PriorityCountSerializer(
            priority_counts, many=True)
        # print(completion_serializer.data)
        completion_order = ["TODO", "INPROGRESS", "ONHOLD", "RESOLVED"]
        completion_status_counts = sorted(
            completion_serializer.data, key=lambda x: completion_order.index(x['completion_status']))

        completion_labels = [item['completion_status']
                             for item in completion_status_counts]
        completion_data = [item['count'] for item in completion_status_counts]

        priority_labels = [item['priority']
                           for item in priority_serializer.data]
        priority_data = [item['count'] for item in priority_serializer.data]

        return Response({
            'completion_status_counts': {
                'labels': completion_labels,
                'datasets': [{
                    'label': 'Tasks by Status',
                    'data': completion_data,
                    'backgroundColor': [
                        "rgba(176, 22, 22, 0.8)",
                        "rgba(153, 102, 255, 0.2)",
                        "rgba(153, 102, 100, 0.2)",
                        "rgba(28, 168, 112, 0.8)",
                    ],
                    'borderColor': [
                        "rgba(255, 99, 132, 1)",
                        "rgba(153, 102, 255, 0.2)",
                        "rgba(153, 102, 100, 0.2)",
                        "rgba(153, 102, 0, 0.2)",
                    ],
                    'options': {
                        'responsive':'true',
                        'maintainAspectRatio': 'false'
                    }
                }]
            },
            'priority_counts': {
                'labels': priority_labels,
                'datasets': [{
                    'label': 'Tasks by Priority',
                    'data': priority_data,
                    'backgroundColor': [
                        "rgba(101, 123, 168, 0.8)",
                        "rgba(28, 123, 168, 0.8)",
                        "rgba(153, 102, 255, 0.2)",
                        "rgba(171, 28, 111, 0.8)",
                        "rgba(176, 22, 22, 0.8)",
                    ],
                    'borderColor': [
                        "rgba(101, 123, 168, 0.8)",
                        "rgba(28, 123, 168, 0.8)",
                        "rgba(153, 102, 255, 0.2)",
                        "rgba(171, 28, 111, 0.8)",
                        "rgba(176, 22, 22, 0.8)",
                    ],
                    'options': {
                        'maintainAspectRatio': 'false'
                    }
                }]
            }
        })
