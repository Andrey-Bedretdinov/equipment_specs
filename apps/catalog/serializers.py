from decimal import Decimal

from rest_framework import serializers

from .models import CatalogItem, CatalogUnit, CatalogUnitItem, CatalogKTS, CatalogKTSUnit, CatalogKTSItem


# ————— Изделие —————

class CatalogItemSerializer(serializers.ModelSerializer):
    """
    Сериализатор для чтения информации об изделии.

    Отдаёт:
    - id: идентификатор изделия
    - name: наименование изделия
    - description: описание изделия
    - supplier: поставщик
    - catalog_code: артикул
    - price: цена за единицу
    - currency: валюта цены
    - manufactured: производитель
    - delivery_type: тип поставки
    """

    class Meta:
        model = CatalogItem
        fields = [
            'id', 'name', 'description', 'supplier', 'catalog_code',
            'price', 'currency', 'manufactured', 'delivery_type'
        ]


class CatalogItemCreateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания нового изделия.

    Принимает:
    - name: наименование изделия (обязательное)
    - description: описание изделия (опционально)
    - supplier: поставщик
    - catalog_code: артикул
    - price: цена
    - currency: валюта
    - manufactured: производитель
    - delivery_type: тип поставки
    """

    class Meta:
        model = CatalogItem
        fields = [
            'name', 'description', 'supplier', 'catalog_code',
            'price', 'currency', 'manufactured', 'delivery_type'
        ]


# ————— Изделия внутри юнита —————

class CatalogUnitItemSerializer(serializers.Serializer):
    """
    Сериализатор изделия внутри юнита (read only).

    Отдаёт:
    - id: идентификатор изделия
    - name: наименование
    - description: описание
    - supplier: поставщик
    - catalog_code: артикул
    - price: цена за все штуки (цена * quantity)
    - currency: валюта
    - manufactured: производитель
    - delivery_type: тип поставки
    - quantity: количество изделий
    """
    id = serializers.IntegerField(source='item.id')
    name = serializers.CharField(source='item.name')
    description = serializers.CharField(source='item.description')
    supplier = serializers.CharField(source='item.supplier')
    catalog_code = serializers.CharField(source='item.catalog_code')
    price = serializers.SerializerMethodField()
    currency = serializers.CharField(source='item.currency')
    manufactured = serializers.CharField(source='item.manufactured')
    delivery_type = serializers.CharField(source='item.delivery_type')
    quantity = serializers.IntegerField()

    def get_price(self, obj):
        total_price = Decimal(obj.item.price) * obj.quantity
        return f"{total_price:.2f}"


# ————— Юнит с изделиями —————

class CatalogUnitSerializer(serializers.ModelSerializer):
    """
    Сериализатор юнита с вложенными изделиями.

    Отдаёт:
    - id: идентификатор юнита
    - name: наименование юнита
    - description: описание юнита
    - price: общая цена юнита (цена всех изделий)
    - items_list: список изделий внутри юнита
    """
    price = serializers.SerializerMethodField()
    items_list = serializers.SerializerMethodField()

    class Meta:
        model = CatalogUnit
        fields = ['id', 'name', 'description', 'price', 'items_list']

    def get_items_list(self, obj):
        unit_items = CatalogUnitItem.objects.filter(unit=obj)
        return CatalogUnitItemSerializer(unit_items, many=True).data

    def get_price(self, obj):
        unit_items = CatalogUnitItem.objects.filter(unit=obj)
        total = sum(Decimal(item.item.price) * item.quantity for item in unit_items)
        return f"{total:.2f}"


class CatalogUnitCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания и редактирования юнита.

    Поля:
    - name: наименование юнита
    - description: описание юнита
    """

    class Meta:
        model = CatalogUnit
        fields = ['id', 'name', 'description']
        read_only_fields = ['id']


class AddItemsToUnitSerializer(serializers.Serializer):
    id = serializers.IntegerField()  # ID юнита
    items = serializers.ListField(
        child=serializers.DictField(
            child=serializers.IntegerField(),
        )
    )

    def validate_items(self, value):
        if not value:
            raise serializers.ValidationError("Список изделий не может быть пустым.")
        for item in value:
            if "id" not in item:
                raise serializers.ValidationError("У каждого изделия должен быть 'id'.")
        return value


# ————— Юнит внутри КТС —————

class CatalogKTSUnitSerializer(serializers.Serializer):
    id = serializers.IntegerField(source='unit.id')
    name = serializers.CharField(source='unit.name')
    description = serializers.CharField(source='unit.description')
    quantity = serializers.IntegerField()
    price = serializers.SerializerMethodField()
    items_list = serializers.SerializerMethodField()

    def get_price(self, obj):
        unit_items = CatalogUnitItem.objects.filter(unit=obj.unit)
        total = sum(Decimal(item.item.price) * item.quantity for item in unit_items)
        final_price = total * obj.quantity
        return f"{final_price:.2f}"

    def get_items_list(self, obj):
        unit_items = CatalogUnitItem.objects.filter(unit=obj.unit)
        return CatalogUnitItemSerializer(unit_items, many=True).data


# ————— Изделие внутри КТС —————

class CatalogKTSItemSerializer(serializers.Serializer):
    """
    Сериализатор изделия внутри КТС.

    Отдаёт:
    - id: идентификатор изделия
    - name: наименование
    - description: описание
    - supplier: поставщик
    - catalog_code: артикул
    - price: цена за все изделия (цена * quantity)
    - currency: валюта
    - manufactured: производитель
    - delivery_type: тип поставки
    - quantity: количество изделий
    """
    id = serializers.IntegerField(source='item.id')
    name = serializers.CharField(source='item.name')
    description = serializers.CharField(source='item.description')
    supplier = serializers.CharField(source='item.supplier')
    catalog_code = serializers.CharField(source='item.catalog_code')
    price = serializers.SerializerMethodField()
    currency = serializers.CharField(source='item.currency')
    manufactured = serializers.CharField(source='item.manufactured')
    delivery_type = serializers.CharField(source='item.delivery_type')
    quantity = serializers.IntegerField()

    def get_price(self, obj):
        total_price = Decimal(obj.item.price) * obj.quantity
        return f"{total_price:.2f}"


# ————— КТС с юнитами и изделиями —————

class CatalogKTSSerializer(serializers.ModelSerializer):
    """
    Сериализатор КТС.

    Отдаёт:
    - id: идентификатор КТС
    - name: наименование
    - description: описание
    - price: общая цена всех юнитов и изделий
    - units_list: список юнитов
    - items_list: список изделий
    """
    units_list = serializers.SerializerMethodField()
    items_list = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()

    class Meta:
        model = CatalogKTS
        fields = ['id', 'name', 'description', 'price', 'units_list', 'items_list']

    def get_units_list(self, obj):
        kts_units = CatalogKTSUnit.objects.filter(kts=obj)
        return CatalogKTSUnitSerializer(kts_units, many=True).data

    def get_items_list(self, obj):
        kts_items = CatalogKTSItem.objects.filter(kts=obj)
        return CatalogKTSItemSerializer(kts_items, many=True).data

    def get_price(self, obj):
        total = Decimal('0.0')

        # сумма юнитов
        kts_units = CatalogKTSUnit.objects.filter(kts=obj)
        for unit in kts_units:
            unit_items = CatalogUnitItem.objects.filter(unit=unit.unit)
            unit_total = sum(Decimal(item.item.price) * item.quantity for item in unit_items)
            total += unit_total * unit.quantity

        # сумма изделий
        kts_items = CatalogKTSItem.objects.filter(kts=obj)
        total += sum(Decimal(item.item.price) * item.quantity for item in kts_items)

        return f"{total:.2f}"


class CatalogKTSCreateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания КТС.

    Поля:
    - name: наименование КТС
    - description: описание КТС
    """

    class Meta:
        model = CatalogKTS
        fields = ['name', 'description']


class AddElementsToKTSSerializer(serializers.Serializer):
    """
    тело POST /catalog/kts/add-elements
    {
        "kts_id": 12,
        "items": [
            {"item_id": 33, "quantity": 3},
            {"item_id": 43, "quantity": 2},
            {"item_id": 4}
        ],
        "units": [
            {"unit_id": 2, "quantity": 2},
            {"unit_id": 3, "quantity": 2},
            {"unit_id": 4}
        ]
    }
    """
    kts_id = serializers.IntegerField()
    items = serializers.ListField(
        child=serializers.DictField(child=serializers.IntegerField()),
        required=False
    )
    units = serializers.ListField(
        child=serializers.DictField(child=serializers.IntegerField()),
        required=False
    )

    def validate(self, attrs):
        # нужны хотя бы items или units
        if not attrs.get("items") and not attrs.get("units"):
            raise serializers.ValidationError("нужно передать items или/и units")
        return attrs
