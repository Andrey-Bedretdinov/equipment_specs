from rest_framework import serializers
from .models import CatalogItem, CatalogUnit, CatalogUnitItem, CatalogKTS, CatalogKTSUnit, CatalogKTSItem


class CatalogItemSerializer(serializers.ModelSerializer):
    """Сериализатор для просмотра изделия"""

    class Meta:
        model = CatalogItem
        fields = [
            'id', 'name', 'description', 'supplier', 'catalog_code',
            'price', 'currency', 'manufactured', 'delivery_type'
        ]


class CatalogItemCreateUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания и обновления изделия"""

    class Meta:
        model = CatalogItem
        fields = [
            'id', 'name', 'description', 'supplier', 'catalog_code',
            'price', 'currency', 'manufactured', 'delivery_type'
        ]
        read_only_fields = ['id']


class CatalogUnitItemSerializer(serializers.ModelSerializer):
    """Сериализатор для изделия в юните (с вложенным изделием)"""
    item = CatalogItemSerializer(read_only=True)

    class Meta:
        model = CatalogUnitItem
        fields = ['id', 'item', 'quantity']


class CatalogUnitItemCreateUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания и обновления изделия в юните"""

    class Meta:
        model = CatalogUnitItem
        fields = ['id', 'unit', 'item', 'quantity']
        read_only_fields = ['id']


class CatalogUnitSerializer(serializers.ModelSerializer):
    """Сериализатор для просмотра юнита с изделиями"""
    items = serializers.SerializerMethodField()

    class Meta:
        model = CatalogUnit
        fields = ['id', 'name', 'description', 'items']

    def get_items(self, obj):
        unit_items = CatalogUnitItem.objects.filter(unit=obj)
        return CatalogUnitItemSerializer(unit_items, many=True).data


class CatalogUnitCreateUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания и обновления юнита"""

    class Meta:
        model = CatalogUnit
        fields = ['id', 'name', 'description']
        read_only_fields = ['id']


class CatalogKTSUnitSerializer(serializers.ModelSerializer):
    """Сериализатор для юнита в КТС (с вложенным юнитом)"""
    unit = CatalogUnitSerializer(read_only=True)

    class Meta:
        model = CatalogKTSUnit
        fields = ['id', 'unit', 'quantity']


class CatalogKTSUnitCreateUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания и обновления юнита в КТС"""

    class Meta:
        model = CatalogKTSUnit
        fields = ['id', 'kts', 'unit', 'quantity']
        read_only_fields = ['id']


class CatalogKTSItemSerializer(serializers.ModelSerializer):
    """Сериализатор для изделия в КТС (с вложенным изделием)"""
    item = CatalogItemSerializer(read_only=True)

    class Meta:
        model = CatalogKTSItem
        fields = ['id', 'item', 'quantity']


class CatalogKTSItemCreateUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания и обновления изделия в КТС"""

    class Meta:
        model = CatalogKTSItem
        fields = ['id', 'kts', 'item', 'quantity']
        read_only_fields = ['id']


class CatalogKTSSerializer(serializers.ModelSerializer):
    """Сериализатор для просмотра КТС с юнитами и изделиями"""
    units = serializers.SerializerMethodField()
    items = serializers.SerializerMethodField()

    class Meta:
        model = CatalogKTS
        fields = ['id', 'name', 'description', 'units', 'items']

    def get_units(self, obj):
        kts_units = CatalogKTSUnit.objects.filter(kts=obj)
        return CatalogKTSUnitSerializer(kts_units, many=True).data

    def get_items(self, obj):
        kts_items = CatalogKTSItem.objects.filter(kts=obj)
        return CatalogKTSItemSerializer(kts_items, many=True).data


class CatalogKTSCreateUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания и обновления КТС"""

    class Meta:
        model = CatalogKTS
        fields = ['id', 'name', 'description']
        read_only_fields = ['id']