from django.db import models


class CatalogItem(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название изделия')
    description = models.TextField(blank=True, verbose_name='Описание изделия')
    supplier = models.CharField(max_length=255, verbose_name='Поставщик')
    catalog_code = models.CharField(max_length=255, verbose_name='Каталожный код')
    price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Цена')
    currency = models.CharField(max_length=10, verbose_name='Валюта')
    manufactured = models.CharField(max_length=255, verbose_name='Производитель')
    delivery_type = models.CharField(max_length=255, verbose_name='Тип доставки')

    def __str__(self):
        return f"{self.name} ({self.catalog_code})"

    class Meta:
        verbose_name = 'Изделие'
        verbose_name_plural = 'Изделия'


class CatalogUnit(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название юнита')
    description = models.TextField(blank=True, verbose_name='Описание юнита')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Комплектная единица (Юнит)'
        verbose_name_plural = 'Комплектные единицы (Юниты)'


class CatalogUnitItem(models.Model):
    unit = models.ForeignKey(CatalogUnit, on_delete=models.CASCADE, related_name='items', verbose_name='Юнит')
    item = models.ForeignKey(CatalogItem, on_delete=models.CASCADE, verbose_name='Изделие')
    quantity = models.PositiveIntegerField(verbose_name='Количество изделий')

    def __str__(self):
        return f"{self.quantity} x {self.item.name} в {self.unit.name}"

    class Meta:
        verbose_name = 'Изделие в юните'
        verbose_name_plural = 'Изделия в юните'


class CatalogKTS(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название КТС')
    description = models.TextField(blank=True, verbose_name='Описание КТС')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Комплекс технических средств (КТС)'
        verbose_name_plural = 'Комплексы технических средств (КТС)'


class CatalogKTSUnit(models.Model):
    kts = models.ForeignKey(CatalogKTS, on_delete=models.CASCADE, related_name='units', verbose_name='КТС')
    unit = models.ForeignKey(CatalogUnit, on_delete=models.CASCADE, verbose_name='Юнит')
    quantity = models.PositiveIntegerField(verbose_name='Количество юнитов')

    def __str__(self):
        return f"{self.quantity} x {self.unit.name} в {self.kts.name}"

    class Meta:
        verbose_name = 'Юнит в КТС'
        verbose_name_plural = 'Юниты в КТС'


class CatalogKTSItem(models.Model):
    kts = models.ForeignKey(CatalogKTS, on_delete=models.CASCADE, related_name='items', verbose_name='КТС')
    item = models.ForeignKey(CatalogItem, on_delete=models.CASCADE, verbose_name='Изделие')
    quantity = models.PositiveIntegerField(verbose_name='Количество изделий')

    def __str__(self):
        return f"{self.quantity} x {self.item.name} в {self.kts.name}"

    class Meta:
        verbose_name = 'Изделие в КТС'
        verbose_name_plural = 'Изделия в КТС'
