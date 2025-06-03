from django.contrib.auth import get_user_model
from django.db import models

from apps.catalog.models import CatalogKTS

User = get_user_model()

class Project(models.Model):
    """
    Проект.

    Описывает конкретный проект, который состоит из одного или нескольких комплексов технических средств (КТС).
    """
    name = models.CharField(
        max_length=255,
        help_text="Название проекта"
    )
    description = models.TextField(
        blank=True,
        help_text="Описание проекта"
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='projects',
        help_text="Пользователь, создавший проект"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Дата и время создания проекта"
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Проект"
        verbose_name_plural = "Проекты"

    def __str__(self):
        return self.name


class ProjectKTS(models.Model):
    """
    Связь проекта с КТС.

    Позволяет добавлять комплексы технических средств (КТС) в проект.
    """
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='project_kts',
        help_text="Проект, к которому привязан КТС"
    )
    catalog_kts = models.ForeignKey(
        CatalogKTS,
        on_delete=models.CASCADE,
        help_text="КТС из справочника"
    )

    class Meta:
        verbose_name = "КТС проекта"
        verbose_name_plural = "КТС проектов"

    def __str__(self):
        return f"{self.project.name} — {self.catalog_kts.name}"
