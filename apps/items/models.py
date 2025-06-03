from apps.catalog.models import CatalogItem
from django.db import models
from apps.units.models import ProjectUnit


class ProjectItem(models.Model):
    """
    Проектное изделие.

    Представляет собой привязку изделия из справочника (CatalogItem)
    к конкретной комплектной единице проекта (ProjectUnit) с указанием количества.
    """

    project_unit = models.ForeignKey(
        ProjectUnit,
        on_delete=models.CASCADE,
        related_name='project_items',
        verbose_name='Комплектная единица проекта'
    )
    catalog_item = models.ForeignKey(
        CatalogItem,
        on_delete=models.PROTECT,
        related_name='used_in_projects',
        verbose_name='Изделие из справочника'
    )
    quantity = models.PositiveIntegerField(
        verbose_name='Количество',
        help_text='Количество изделий в проектной спецификации'
    )

    class Meta:
        verbose_name = 'Проектное изделие'
        verbose_name_plural = 'Проектные изделия'
        ordering = ['id']

    def __str__(self):
        return f"{self.catalog_item.name} (x{self.quantity})"
