from rest_framework import serializers

from apps.catalog.models import CatalogUnit
from apps.units.models import ProjectUnit


class CatalogUnitSerializer(serializers.ModelSerializer):
    """
    Сериализатор для справочника комплектных единиц.
    Используется для вложенного отображения информации о юните.
    """

    class Meta:
        model = CatalogUnit
        fields = ['id', 'name']


class ProjectUnitSerializer(serializers.ModelSerializer):
    """
    Сериализатор для комплектной единицы проекта.
    """

    catalog_unit = CatalogUnitSerializer(read_only=True)
    catalog_unit_id = serializers.PrimaryKeyRelatedField(
        queryset=CatalogUnit.objects.all(),
        source='catalog_unit',
        write_only=True
    )

    class Meta:
        model = ProjectUnit
        fields = [
            'id',
            'project_kts',
            'catalog_unit',
            'catalog_unit_id',
            'quantity'
        ]
        extra_kwargs = {
            'project_kts': {'help_text': 'ID проектного КТС, к которому привязан юнит'},
            'catalog_unit': {'help_text': 'Детали комплектной единицы из справочника (read-only)'},
            'catalog_unit_id': {'help_text': 'ID комплектной единицы из справочника (для записи)'},
            'quantity': {'help_text': 'Количество комплектных единиц в проекте'}
        }