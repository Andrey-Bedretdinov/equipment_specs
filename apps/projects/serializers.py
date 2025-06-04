from rest_framework import serializers

from apps.catalog.models import CatalogUnitItem, CatalogKTSUnit, CatalogKTSItem
from .models import Project, ProjectKTS, ProjectUnit, ProjectItem


# изделие
class ItemSerializer(serializers.Serializer):
    id = serializers.IntegerField(source='item.id')
    name = serializers.CharField(source='item.name')
    description = serializers.CharField(source='item.description')
    supplier = serializers.CharField()
    catalog_code = serializers.CharField()
    price = serializers.DecimalField(max_digits=12, decimal_places=2)
    currency = serializers.CharField()
    manufactured = serializers.CharField()
    delivery_type = serializers.CharField()
    quantity = serializers.IntegerField()


# юнит с изделиями
class UnitWithItemsSerializer(serializers.Serializer):
    id = serializers.IntegerField(source='unit.id')
    name = serializers.CharField(source='unit.name')
    description = serializers.CharField(source='unit.description')
    quantity = serializers.IntegerField()
    items_list = serializers.SerializerMethodField()  # <-- ПРАВИЛЬНО

    def get_items_list(self, obj):  # <-- И метод тоже переименовать!
        unit_items = CatalogUnitItem.objects.filter(unit=obj.unit)
        return [
            {
                "id": item.item.id,
                "name": item.item.name,
                "description": item.item.description,
                "supplier": item.item.supplier,
                "catalog_code": item.item.catalog_code,
                "price": item.item.price,
                "currency": item.item.currency,
                "manufactured": item.item.manufactured,
                "delivery_type": item.item.delivery_type,
                "quantity": item.quantity
            }
            for item in unit_items
        ]


# ктс с юнитами и изделиями
class KTSWithUnitsItemsSerializer(serializers.Serializer):
    id = serializers.IntegerField(source='kts.id')
    name = serializers.CharField(source='kts.name')
    description = serializers.CharField(source='kts.description')
    quantity = serializers.IntegerField()
    units_list = serializers.SerializerMethodField()
    items_list = serializers.SerializerMethodField()

    def get_units_list(self, obj):
        kts_units = CatalogKTSUnit.objects.filter(kts=obj.kts)
        return [
            {
                "id": unit.unit.id,
                "name": unit.unit.name,
                "description": unit.unit.description,
                "quantity": unit.quantity,
                "items_list": [
                    {
                        "id": item.item.id,
                        "name": item.item.name,
                        "description": item.item.description,
                        "supplier": item.item.supplier,
                        "catalog_code": item.item.catalog_code,
                        "price": item.item.price,
                        "currency": item.item.currency,
                        "manufactured": item.item.manufactured,
                        "delivery_type": item.item.delivery_type,
                        "quantity": item.quantity
                    }
                    for item in CatalogUnitItem.objects.filter(unit=unit.unit)
                ]
            }
            for unit in kts_units
        ]

    def get_items_list(self, obj):
        kts_items = CatalogKTSItem.objects.filter(kts=obj.kts)
        return [
            {
                "id": item.item.id,
                "name": item.item.name,
                "description": item.item.description,
                "supplier": item.item.supplier,
                "catalog_code": item.item.catalog_code,
                "price": item.item.price,
                "currency": item.item.currency,
                "manufactured": item.item.manufactured,
                "delivery_type": item.item.delivery_type,
                "quantity": item.quantity
            }
            for item in kts_items
        ]


# изделие напрямую в проекте
class ProjectItemSerializer(serializers.Serializer):
    id = serializers.IntegerField(source='item.id')
    name = serializers.CharField(source='item.name')
    description = serializers.CharField(source='item.description')
    supplier = serializers.CharField(source='item.supplier')
    catalog_code = serializers.CharField(source='item.catalog_code')
    price = serializers.DecimalField(source='item.price', max_digits=12, decimal_places=2)
    currency = serializers.CharField(source='item.currency')
    manufactured = serializers.CharField(source='item.manufactured')
    delivery_type = serializers.CharField(source='item.delivery_type')
    quantity = serializers.IntegerField()


# основной проект
class ProjectSerializer(serializers.ModelSerializer):
    kts_list = serializers.SerializerMethodField()
    units_list = serializers.SerializerMethodField()
    items_list = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'kts_list', 'units_list', 'items_list']

    def get_kts_list(self, obj):
        kts = ProjectKTS.objects.filter(project=obj)
        return KTSWithUnitsItemsSerializer(kts, many=True).data

    def get_units_list(self, obj):
        units = ProjectUnit.objects.filter(project=obj)
        return UnitWithItemsSerializer(units, many=True).data

    def get_items_list(self, obj):
        items = ProjectItem.objects.filter(project=obj)
        return ProjectItemSerializer(items, many=True).data