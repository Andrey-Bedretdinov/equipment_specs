from rest_framework import serializers
from .models import CatalogItem, CatalogUnit, CatalogUnitItem, CatalogKTS, CatalogKTSUnit, CatalogKTSItem


class CatalogItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CatalogItem
        fields = [
            'id', 'name', 'description', 'supplier', 'catalog_code',
            'price', 'currency', 'manufactured', 'delivery_type'
        ]


class CatalogUnitItemSerializer(serializers.ModelSerializer):
    item = CatalogItemSerializer(read_only=True)

    class Meta:
        model = CatalogUnitItem
        fields = ['id', 'item', 'quantity']


class CatalogUnitSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()

    class Meta:
        model = CatalogUnit
        fields = ['id', 'name', 'description', 'items']

    def get_items(self, obj):
        unit_items = CatalogUnitItem.objects.filter(unit=obj)
        return CatalogUnitItemSerializer(unit_items, many=True).data


class CatalogKTSUnitSerializer(serializers.ModelSerializer):
    unit = CatalogUnitSerializer(read_only=True)

    class Meta:
        model = CatalogKTSUnit
        fields = ['id', 'unit', 'quantity']


class CatalogKTSItemSerializer(serializers.ModelSerializer):
    item = CatalogItemSerializer(read_only=True)

    class Meta:
        model = CatalogKTSItem
        fields = ['id', 'item', 'quantity']


class CatalogKTSSerializer(serializers.ModelSerializer):
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