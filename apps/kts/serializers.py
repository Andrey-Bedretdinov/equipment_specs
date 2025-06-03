from rest_framework import serializers

from .models import ProjectKTS


class ProjectKTSSerializer(serializers.ModelSerializer):
    """
    Сериализатор для КТС проекта.

    Позволяет управлять привязкой КТС из справочника к проекту.
    """

    class Meta:
        model = ProjectKTS
        fields = ['id', 'project', 'catalog_kts']
        extra_kwargs = {
            'project': {'help_text': 'ID проекта'},
            'catalog_kts': {'help_text': 'ID КТС из справочника'}
        }
