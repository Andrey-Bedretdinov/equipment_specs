from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import ProjectItem
from .serializers import ProjectItemSerializer


@extend_schema_view(
    list=extend_schema(summary="Список проектных изделий"),
    retrieve=extend_schema(summary="Детали проектного изделия"),
    create=extend_schema(summary="Добавить проектное изделие"),
    update=extend_schema(summary="Обновить проектное изделие"),
    partial_update=extend_schema(summary="Частичное обновление проектного изделия"),
    destroy=extend_schema(summary="Удалить проектное изделие"),
)
class ProjectItemViewSet(viewsets.ModelViewSet):
    """
    Управление изделиями внутри проектных комплектных единиц.
    """

    serializer_class = ProjectItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        project_unit_id = self.kwargs.get('project_unit_pk')
        if project_unit_id:
            return ProjectItem.objects.filter(project_unit_id=project_unit_id)
        return ProjectItem.objects.all()

    def perform_create(self, serializer):
        project_unit_id = self.kwargs.get('project_unit_pk')
        serializer.save(project_unit_id=project_unit_id)
