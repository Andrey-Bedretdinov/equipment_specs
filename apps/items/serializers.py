from apps.catalog.serializers import CatalogItemSerializer
from rest_framework import serializers

from .models import ProjectItem


class ProjectItemSerializer(serializers.ModelSerializer):
    """
    Сериализатор для проектного изделия.

    Показывает информацию о выбранном изделии из справочника и количестве в проекте.
    """

    catalog_item = CatalogItemSerializer(read_only=True)
    catalog_item_id = serializers.PrimaryKeyRelatedField(
        queryset=ProjectItem._meta.get_field('catalog_item').remote_field.model.objects.all(),
        source='catalog_item',
        write_only=True,
        help_text='ID изделия из справочника'
    )

    class Meta:
        model = ProjectItem
        fields = [
            'id',
            'project_unit',
            'catalog_item',
            'catalog_item_id',
            'quantity',
        ]
        extra_kwargs = {
            'project_unit': {
                'help_text': 'ID комплектной единицы проекта',
            },
            'quantity': {
                'help_text': 'Количество изделий в проекте',
            }
        }
