from django.db import models


class ProjectKTS(models.Model):
    """
    Комплекс технических средств (КТС) проекта.

    Связывает проект с выбранным КТС из справочника.
    """
    project = models.ForeignKey(
        'projects.Project',
        on_delete=models.CASCADE,
        related_name='kts',
        help_text='Проект, к которому принадлежит этот КТС'
    )
    catalog_kts = models.ForeignKey(
        'catalog.CatalogKTS',
        on_delete=models.PROTECT,
        related_name='project_kts',
        help_text='Справочник КТС'
    )

    class Meta:
        verbose_name = 'КТС проекта'
        verbose_name_plural = 'КТС проектов'

    def __str__(self):
        return f"{self.catalog_kts.name} (проект: {self.project.name})"
