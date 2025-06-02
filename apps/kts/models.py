from django.db import models

from apps.projects.models import Project


class KTS(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='kts')
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name} (проект: {self.project.name})"
