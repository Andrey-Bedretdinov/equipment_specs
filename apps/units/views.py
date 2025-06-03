from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated

from apps.units.models import ProjectUnit
from apps.units.serializers import ProjectUnitSerializer


@extend_schema_view(
    list=extend_schema(summary="Список комплектных единиц проекта"),
    retrieve=extend_schema(summary="Детали комплектной единицы"),
    create=extend_schema(summary="Создать комплектную единицу"),
    update=extend_schema(summary="Обновить комплектную единицу"),
    partial_update=extend_schema(summary="Частичное обновление комплектной единицы"),
    destroy=extend_schema(summary="Удалить комплектную единицу"),
)
class ProjectUnitViewSet(viewsets.ModelViewSet):
    """
    Управление комплектными единицами в рамках проектного КТС.
    """

    serializer_class = ProjectUnitSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        project_kts_id = self.kwargs.get('project_kts_pk')
        if project_kts_id:
            return ProjectUnit.objects.filter(project_kts_id=project_kts_id)
        return ProjectUnit.objects.all()

    def perform_create(self, serializer):
        project_kts_id = self.kwargs.get('project_kts_pk')
        if not project_kts_id:
            raise ValidationError({'detail': 'project_kts_pk is required in the URL.'})
        serializer.save(project_kts_id=project_kts_id)
