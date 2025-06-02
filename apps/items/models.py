from django.db import models

from apps.units.models import Unit


class Item(models.Model):
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name='items')
    name = models.CharField(max_length=255)
    supplier = models.CharField(max_length=255)
    catalog_code = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
    manufacturer = models.CharField(max_length=255)
    currency = models.CharField(max_length=10)
    delivery_type = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name} ({self.quantity} шт.)"
