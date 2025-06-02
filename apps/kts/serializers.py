from rest_framework import serializers

from .models import KTS


class KTSSerializer(serializers.ModelSerializer):
    """
    Комплекс технических средств (КТС) — часть проекта.
    """

    class Meta:
        model = KTS
        fields = ['id', 'name', 'project']
        extra_kwargs = {
            'name': {'help_text': 'Название КТС'},
            'project': {'help_text': 'ID проекта, к которому принадлежит КТС'}
        }