from django.db import models


class Project(models.Model):
    name = models.CharField(max_length=64, default='project', unique=False)
    description = models.TextField(null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    last_update_on = models.DateTimeField(auto_now=True)

    def get_most_recent_project():
        return Project.objects.latest('last_update_on')



class ProjectTasks(models.Model):
    project = models.ForeignKey("Project", on_delete=models.CASCADE)

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

    def get_most_recent_task():
        return ProjectTasks.objects.latest('last_update_on')
