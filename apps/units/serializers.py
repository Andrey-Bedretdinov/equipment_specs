from rest_framework import serializers

from .models import Unit


class UnitSerializer(serializers.ModelSerializer):
    """
    Комплектная единица — элемент КТС, содержащий изделия.
    """

    class Meta:
        model = Unit
        fields = ['id', 'name', 'kts']
        extra_kwargs = {
            'name': {'help_text': 'Название комплектной единицы'},
            'kts': {'help_text': 'ID КТС, к которому принадлежит комплектная единица'}
        }
