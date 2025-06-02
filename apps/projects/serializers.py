from rest_framework import serializers

from .models import Project


class ProjectSerializer(serializers.ModelSerializer):
    """
    Проект — основная сущность системы.
    Содержит комплексы технических средств (КТС).
    """

    created_by = serializers.ReadOnlyField(source='created_by.id')

    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'created_by', 'created_at']
        extra_kwargs = {
            'name': {'help_text': 'Название проекта'},
            'description': {'help_text': 'Описание проекта'},
            'created_by': {'help_text': 'Пользователь, создавший проект'},
            'created_at': {'help_text': 'Дата и время создания проекта'}
        }
