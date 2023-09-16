from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import ProjectTasks


@receiver(post_save, sender=ProjectTasks)
def update_project_last_updated_on(sender, instance, **kwargs):
    project = instance.project
    project.save()


@receiver(post_delete, sender=ProjectTasks)
def update_project_last_updated_on_delete(sender, instance, **kwargs):
    project = instance.project
    project.save()
