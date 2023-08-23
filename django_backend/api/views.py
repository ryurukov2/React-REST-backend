from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Project, ProjectTasks
from .serializers import ProjectSerializer, TaskSerializer
from rest_framework.authentication import TokenAuthentication


class CreateProjectsView(generics.CreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


class ListProjectsView(generics.ListAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


class ProjectDeleteView(generics.DestroyAPIView):
    
    serializer_class = ProjectSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        project_id=self.kwargs['pk']
        return Project.objects.filter(id=project_id)

class ProjectDetailView(generics.RetrieveAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = ProjectSerializer

    def get_queryset(self):
        task_id=self.kwargs['pk']
        return Project.objects.filter(id=task_id)

class TasksListView(generics.ListAPIView):
    serializer_class = TaskSerializer
    pagination_class = None
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


    def get_queryset(self):
        project_id = self.kwargs['project_id']
        return ProjectTasks.objects.filter(project__id=project_id)
    
    
class TasksCreateView(generics.CreateAPIView):
    serializer_class = TaskSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


class TasksEditView(generics.UpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = TaskSerializer
    def get_queryset(self):
        task_id=self.kwargs['pk']
        return ProjectTasks.objects.filter(id=task_id)


class TasksDeleteView(generics.DestroyAPIView):
    serializer_class = TaskSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        task_id=self.kwargs['pk']
        return ProjectTasks.objects.filter(id=task_id)
    

class TaskGetLastEditedView(generics.ListAPIView):
    serializer_class_ProjectTasks = TaskSerializer
    serializer_class_Project = ProjectSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get_queryset_ProjectTasks(self):
        last_task = ProjectTasks.get_most_recent_task()
        return ProjectTasks.objects.filter(project=last_task.project).order_by('-last_update_on')
    def get_queryset_Project(self, id):
        # last_project = Project.get_most_recent_project()
        # print(last_project.id)
        return Project.objects.get(id=id)


    def list(self, request, *args, **kwargs):
        print(request.headers['Authorization'])
        print(f'a {request.user}')
        tasks = self.serializer_class_ProjectTasks(self.get_queryset_ProjectTasks(), many=True)
        project = self.serializer_class_Project(self.get_queryset_Project(tasks.data[0]['project']), many=False)
        return Response({"project": project.data,
                         "tasks": tasks.data})
    