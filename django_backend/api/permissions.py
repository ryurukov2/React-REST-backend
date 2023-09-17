from rest_framework import permissions

from .models import Project, ProjectTasks


class IsProjectOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):

        if(type(obj)==Project):
            return obj.owner == request.user
        elif(type(obj==ProjectTasks)):
            return obj.project.owner == request.user
    
class IsProjectOwnerOrAssigned(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if(type(obj)==Project):
            result = (obj.owner == request.user or request.user in obj.assigned.all())
        elif(type(obj==ProjectTasks)):
            print(obj.project.owner)
            result = (obj.project.owner == request.user or request.user in obj.project.assigned.all())
        # print(result)
        return result 

