from django.db import models

from apps.kts.models import KTS


class Unit(models.Model):
    kts = models.ForeignKey(KTS, on_delete=models.CASCADE, related_name='units')
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name} (КТС: {self.kts.name})"
