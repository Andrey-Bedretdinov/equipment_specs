from django.db import models

from apps.catalog.models import CatalogUnit
from apps.kts.models import ProjectKTS


class ProjectUnit(models.Model):
    """
    Проектная комплектная единица (юнит).
    Связывает проектный КТС с шаблонной комплектной единицей (справочник CatalogUnit).
    """

    project_kts = models.ForeignKey(
        ProjectKTS,
        on_delete=models.CASCADE,
        related_name='units',
        verbose_name='КТС проекта'
    )
    catalog_unit = models.ForeignKey(
        CatalogUnit,
        on_delete=models.CASCADE,
        related_name='project_units',
        verbose_name='Справочник комплектных единиц'
    )
    quantity = models.PositiveIntegerField(
        default=1,
        verbose_name='Количество единиц'
    )

    class Meta:
        verbose_name = 'Комплектная единица проекта'
        verbose_name_plural = 'Комплектные единицы проекта'

    def __str__(self):
        return f"{self.catalog_unit.name} (КТС: {self.project_kts.catalog_kts.name}, Кол-во: {self.quantity})"
