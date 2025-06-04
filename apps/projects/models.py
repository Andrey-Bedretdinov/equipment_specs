from django.db import models

from apps.catalog.models import CatalogItem, CatalogUnit, CatalogKTS


class Project(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название проекта')
    description = models.TextField(blank=True, verbose_name='Описание проекта')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'


class ProjectKTS(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='kts', verbose_name='Проект')
    kts = models.ForeignKey(CatalogKTS, on_delete=models.CASCADE, verbose_name='КТС', null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество КТС')

    def __str__(self):
        return f"{self.quantity} x {self.kts.name} в {self.project.name}"

    class Meta:
        verbose_name = 'КТС в проекте'
        verbose_name_plural = 'КТС в проекте'


class ProjectUnit(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='units', verbose_name='Проект')
    unit = models.ForeignKey(CatalogUnit, on_delete=models.CASCADE, verbose_name='Юнит', null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество юнитов')

    def __str__(self):
        return f"{self.quantity} x {self.unit.name} в {self.project.name}"

    class Meta:
        verbose_name = 'Юнит в проекте'
        verbose_name_plural = 'Юниты в проекте'


class ProjectItem(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='items', verbose_name='Проект')
    item = models.ForeignKey(CatalogItem, on_delete=models.CASCADE, verbose_name='Изделие', null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество изделий')

    def __str__(self):
        return f"{self.quantity} x {self.item.name} в {self.project.name}"

    class Meta:
        verbose_name = 'Изделие в проекте'
        verbose_name_plural = 'Изделия в проекте'
