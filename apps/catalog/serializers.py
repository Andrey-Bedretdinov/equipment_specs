from rest_framework import serializers
from .models import CatalogItem, CatalogUnit, CatalogUnitItem, CatalogKTS, CatalogKTSUnit, CatalogKTSItem


class CatalogItemSerializer(serializers.ModelSerializer):
    """
    Сериализатор для изделия (CatalogItem).

    Поля:
    - id: идентификатор изделия
    - name: наименование
    - description: описание изделия
    - supplier: поставщик
    - catalog_code: артикул (код в каталоге)
    - price: цена за единицу
    - currency: валюта цены
    - manufactured: производитель
    - delivery_type: способ поставки (склад/под заказ)
    """

    class Meta:
        model = CatalogItem
        fields = [
            'id', 'name', 'description', 'supplier', 'catalog_code',
            'price', 'currency', 'manufactured', 'delivery_type'
        ]


class CatalogUnitItemSerializer(serializers.ModelSerializer):
    """
    Сериализатор для изделия в юните (CatalogUnitItem).

    Поля:
    - id: идентификатор связи юнита и изделия
    - item: вложенный сериализатор изделия
    - quantity: количество изделий в юните
    """

    item = CatalogItemSerializer(read_only=True)

    class Meta:
        model = CatalogUnitItem
        fields = ['id', 'item', 'quantity']


class CatalogUnitSerializer(serializers.ModelSerializer):
    """
    Сериализатор для юнита (CatalogUnit).

    Поля:
    - id: идентификатор юнита
    - name: наименование юнита
    - description: описание юнита
    - items: список изделий в юните
    """

    items = serializers.SerializerMethodField()

    class Meta:
        model = CatalogUnit
        fields = ['id', 'name', 'description', 'items']

    def get_items(self, obj):
        """
        Получает список изделий в юните.
        """
        unit_items = CatalogUnitItem.objects.filter(unit=obj)
        return CatalogUnitItemSerializer(unit_items, many=True).data


class CatalogKTSUnitSerializer(serializers.ModelSerializer):
    """
    Сериализатор для юнита в КТС (CatalogKTSUnit).

    Поля:
    - id: идентификатор связи КТС и юнита
    - unit: вложенный сериализатор юнита
    - quantity: количество юнитов в КТС
    """

    unit = CatalogUnitSerializer(read_only=True)

    class Meta:
        model = CatalogKTSUnit
        fields = ['id', 'unit', 'quantity']


class CatalogKTSItemSerializer(serializers.ModelSerializer):
    """
    Сериализатор для изделия в КТС (CatalogKTSItem).

    Поля:
    - id: идентификатор связи КТС и изделия
    - item: вложенный сериализатор изделия
    - quantity: количество изделий в КТС
    """

    item = CatalogItemSerializer(read_only=True)

    class Meta:
        model = CatalogKTSItem
        fields = ['id', 'item', 'quantity']


class CatalogKTSSerializer(serializers.ModelSerializer):
    """
    Сериализатор для КТС (CatalogKTS).

    Поля:
    - id: идентификатор КТС
    - name: наименование КТС
    - description: описание КТС
    - units: список юнитов в КТС
    - items: список изделий в КТС
    """

    units = serializers.SerializerMethodField()
    items = serializers.SerializerMethodField()

    class Meta:
        model = CatalogKTS
        fields = ['id', 'name', 'description', 'units', 'items']

    def get_units(self, obj):
        """
        Получает список юнитов, входящих в КТС.
        """
        kts_units = CatalogKTSUnit.objects.filter(kts=obj)
        return CatalogKTSUnitSerializer(kts_units, many=True).data

    def get_items(self, obj):
        """
        Получает список изделий, входящих в КТС.
        """
        kts_items = CatalogKTSItem.objects.filter(kts=obj)
        return CatalogKTSItemSerializer(kts_items, many=True).data