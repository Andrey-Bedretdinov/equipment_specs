from rest_framework import serializers
from .models import Item


class ItemSerializer(serializers.ModelSerializer):
    """
    Изделие — элемент комплектной единицы.
    """

    class Meta:
        model = Item
        fields = [
            'id', 'unit', 'name', 'supplier', 'catalog_code',
            'quantity', 'price', 'manufacturer', 'currency', 'delivery_type'
        ]
        extra_kwargs = {
            'unit': {'help_text': 'ID комплектной единицы, к которой относится изделие'},
            'name': {'help_text': 'Название изделия'},
            'supplier': {'help_text': 'Поставщик изделия'},
            'catalog_code': {'help_text': 'Каталожный номер изделия'},
            'quantity': {'help_text': 'Количество изделий'},
            'price': {'help_text': 'Цена за единицу'},
            'manufacturer': {'help_text': 'Производитель изделия'},
            'currency': {'help_text': 'Валюта цены'},
            'delivery_type': {'help_text': 'Тип поставки'}
        }
