from django.db import models


class CatalogItem(models.Model):
    """
    Справочник изделий.

    Хранит информацию об изделиях:
    - название,
    - описание,
    - поставщик,
    - каталожный код,
    - цена,
    - валюта,
    - производитель,
    - тип доставки.
    """
    name = models.CharField(max_length=255, verbose_name="Название изделия")
    description = models.TextField(blank=True, verbose_name="Описание изделия")
    supplier = models.CharField(max_length=255, verbose_name="Поставщик")
    catalog_code = models.CharField(max_length=255, verbose_name="Каталожный код")
    price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Цена")
    currency = models.CharField(max_length=10, verbose_name="Валюта")
    manufactured = models.CharField(max_length=255, verbose_name="Производитель")
    delivery_type = models.CharField(max_length=255, verbose_name="Тип доставки")

    class Meta:
        verbose_name = "Изделие"
        verbose_name_plural = "Изделия"
        ordering = ['name']

    def __str__(self):
        return self.name


class CatalogUnit(models.Model):
    """
    Справочник комплектных единиц (юнитов).

    Юнит — это набор изделий, собираемый вместе и используемый как самостоятельная часть КТС.
    """
    name = models.CharField(max_length=255, verbose_name="Название юнита")
    description = models.TextField(blank=True, verbose_name="Описание юнита")

    class Meta:
        verbose_name = "Комплектная единица"
        verbose_name_plural = "Комплектные единицы"
        ordering = ['name']

    def __str__(self):
        return self.name


class CatalogKTS(models.Model):
    """
    Справочник комплексов технических средств (КТС).

    КТС — это группа комплектных единиц, объединённых по функциональному признаку.
    """
    name = models.CharField(max_length=255, verbose_name="Название КТС")
    description = models.TextField(blank=True, verbose_name="Описание КТС")

    class Meta:
        verbose_name = "Комплекс технических средств (КТС)"
        verbose_name_plural = "Комплексы технических средств (КТС)"
        ordering = ['name']

    def __str__(self):
        return self.name
