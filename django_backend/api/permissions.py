from rest_framework import permissions

from .models import Project, ProjectTasks


class IsProjectOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        print('f')

        if(type(obj)==Project):
            return obj.owner == request.user
        elif(type(obj==ProjectTasks)):
            return obj.project.owner == request.user
    
class IsProjectOwnerOrAssigned(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        print('a')
        if(type(obj)==Project):
            _ = (obj.owner == request.user or request.user in obj.assigned.all())
        elif(type(obj==ProjectTasks)):
            print(obj.project.owner)
            _ = (obj.project.owner == request.user or request.user in obj.project.assigned.all())
        # print(_)
        return _ 

