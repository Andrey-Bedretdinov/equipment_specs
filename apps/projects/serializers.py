from rest_framework import serializers

from apps.catalog.serializers import CatalogKTSSerializer
from .models import Project, ProjectKTS


class ProjectSerializer(serializers.ModelSerializer):
    """
    Сериализатор для проекта.

    Представляет базовую информацию о проекте.
    """
    created_by = serializers.ReadOnlyField(source='created_by.id')

    class Meta:
        model = Project
        fields = [
            'id',
            'name',
            'description',
            'created_by',
            'created_at'
        ]
        extra_kwargs = {
            'name': {'help_text': 'Название проекта'},
            'description': {'help_text': 'Описание проекта'},
            'created_by': {'help_text': 'ID пользователя, создавшего проект'},
            'created_at': {'help_text': 'Дата и время создания проекта'}
        }


class ProjectKTSSerializer(serializers.ModelSerializer):
    """
    Сериализатор для КТС, привязанных к проекту.

    Позволяет видеть, какие КТС выбраны для данного проекта.
    """
    catalog_kts = CatalogKTSSerializer(read_only=True)
    catalog_kts_id = serializers.PrimaryKeyRelatedField(
        queryset=ProjectKTS.objects.all(),
        source='catalog_kts',
        write_only=True,
        help_text="ID КТС из справочника, которое будет добавлено в проект"
    )

    class Meta:
        model = ProjectKTS
        fields = [
            'id',
            'project',
            'catalog_kts',
            'catalog_kts_id'
        ]
        extra_kwargs = {
            'project': {'help_text': 'ID проекта'},
            'catalog_kts': {'help_text': 'Детали КТС из справочника', 'read_only': True},
            'catalog_kts_id': {'write_only': True}
        }
