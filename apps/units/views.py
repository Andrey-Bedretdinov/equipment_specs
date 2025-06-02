from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import viewsets
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.permissions import IsAuthenticated

from apps.kts.models import KTS
from .models import Unit
from .serializers import UnitSerializer


@extend_schema_view(
    list=extend_schema(description="Получить список комплектных единиц для КТС."),
    retrieve=extend_schema(description="Получить детали комплектной единицы."),
    create=extend_schema(description="Создать комплектную единицу для КТС."),
    update=extend_schema(description="Обновить комплектную единицу."),
    destroy=extend_schema(description="Удалить комплектную единицу."),
)
class UnitViewSet(viewsets.ModelViewSet):
    """
    Управление комплектными единицами в рамках КТС.
    """
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if 'kts_pk' in self.kwargs:
            return self.queryset.filter(kts_id=self.kwargs['kts_pk'])
        return super().get_queryset()

    def perform_create(self, serializer):
        kts_id = self.kwargs.get('kts_pk')
        if kts_id:
            try:
                kts = KTS.objects.get(pk=kts_id)
            except KTS.DoesNotExist:
                raise NotFound('KTS not found')
            serializer.save(kts=kts)
        else:
            raise ValidationError('KTS id is required')
