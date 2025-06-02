from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import viewsets
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.permissions import IsAuthenticated

from apps.units.models import Unit
from .models import Item
from .serializers import ItemSerializer


@extend_schema_view(
    list=extend_schema(description="Получить список всех изделий комплектной единицы."),
    retrieve=extend_schema(description="Получить детали изделия."),
    create=extend_schema(description="Создать новое изделие."),
    update=extend_schema(description="Обновить изделие."),
    destroy=extend_schema(description="Удалить изделие."),
)
class ItemViewSet(viewsets.ModelViewSet):
    """
    Управление изделиями комплектных единиц.
    """
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if 'unit_pk' in self.kwargs:
            return self.queryset.filter(unit_id=self.kwargs['unit_pk'])
        return super().get_queryset()

    def perform_create(self, serializer):
        unit_id = self.kwargs.get('unit_pk')
        if unit_id:
            try:
                unit = Unit.objects.get(pk=unit_id)
            except Unit.DoesNotExist:
                raise NotFound('Unit not found')
            serializer.save(unit=unit)
        else:
            raise ValidationError('Unit id is required')
