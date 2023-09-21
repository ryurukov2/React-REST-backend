

from django.urls import path

# from .views import CreateProjectsView, ProjectDetailView, TasksListView, TasksCreateView, ListProjectsView, ProjectDeleteView
from .views import *

urlpatterns = [
    path('projects/add', CreateProjectsView.as_view(), name='add projects'),
    path('projects/list', ListProjectsView.as_view(), name='list projects'),
    path('projects/remove/<int:pk>', ProjectDeleteView.as_view(), name='list projects'),
    path('projects/<int:pk>/', ProjectDetailView.as_view(), name='project-detail'),
    path('projects/<int:project_id>/tasks/', TasksListView.as_view(), name='project-tasks-list'),
    path('projects/tasks/add', TasksCreateView.as_view(), name='tasks'),
    path('task/<int:pk>/edit', TasksEditView.as_view(), name='task edit'),
    path('task/<int:pk>/remove', TasksDeleteView.as_view(), name='task edit'),
    path('tasks/last_edited', TaskGetLastEditedView.as_view(), name='last edited'),
    path('projects/<int:pk>/add_assignee', AddAssigneeView.as_view(), name='add assignee'),
    path('projects/<int:pk>/retrieve_owner', RetrieveProjectOwnerView.as_view(), name='retrieve owner'),
    path('projects/<int:pk>/list_assigned', ListProjectAssigned.as_view(), name='list assigned'),
    
    ]