from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q

class Project(models.Model):
    name = models.CharField(max_length=64, default='project', unique=False)
    description = models.TextField(null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner')
    last_update_on = models.DateTimeField(auto_now=True)
    assigned = models.ManyToManyField(User, related_name='assigned')
    def get_most_recent_project(user_id):
        try:
             return Project.objects.filter(Q(owner=user_id)|Q(assigned=user_id)).latest('last_update_on')
        except Exception:
            return None



class ProjectTasks(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    class Priority(models.IntegerChoices):
        VITAL = 5
        URGENT = 4
        IMPORTANT = 3
        CAN_WAIT = 2
        MINOR = 1

    COMPLETION_STATUS_CHOICES = [
        ("TODO", "TODO"),
        ("INPROGRESS", "INPROGRESS"),
        ("ONHOLD", "ONHOLD"),
        ("RESOLVED", "RESOLVED"),
    ]

    description = models.TextField(null=True, blank=True)
    priority = models.IntegerField(choices=Priority.choices)
    completion_status = models.CharField(
        max_length=64, choices=COMPLETION_STATUS_CHOICES, default="TODO", null=False)
    created_on = models.DateTimeField(auto_now_add=True)
    last_update_on = models.DateTimeField(auto_now=True)

    def get_most_recent_task(user_id):
        try:
            return ProjectTasks.objects.filter(Q(project__owner=user_id)|Q(project__assigned=user_id)).latest('last_update_on')
        except Exception as e:
            return None

