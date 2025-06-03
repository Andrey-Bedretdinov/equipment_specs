from rest_framework import serializers

from .models import CatalogItem, CatalogUnit, CatalogKTS


class CatalogItemSerializer(serializers.ModelSerializer):
    """
    Сериализатор для изделия справочника.

    Поля:
    - id: ID изделия
    - name: Название изделия
    - description: Описание изделия
    - supplier: Поставщик
    - catalog_code: Каталожный код
    - price: Цена
    - currency: Валюта
    - manufactured: Производитель
    - delivery_type: Тип доставки
    """

    class Meta:
        model = CatalogItem
        fields = [
            'id', 'name', 'description',
            'supplier', 'catalog_code', 'price',
            'currency', 'manufactured', 'delivery_type'
        ]


class CatalogUnitSerializer(serializers.ModelSerializer):
    """
    Сериализатор для комплектной единицы (юнита) справочника.

    Поля:
    - id: ID юнита
    - name: Название юнита
    - description: Описание юнита
    """

    class Meta:
        model = CatalogUnit
        fields = ['id', 'name', 'description']


class CatalogKTSSerializer(serializers.ModelSerializer):
    """
    Сериализатор для комплекса технических средств (КТС) справочника.

    Поля:
    - id: ID КТС
    - name: Название КТС
    - description: Описание КТС
    """

    class Meta:
        model = CatalogKTS
        fields = ['id', 'name', 'description']
