from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated

from .models import ProjectKTS
from .serializers import ProjectKTSSerializer


@extend_schema_view(
    list=extend_schema(summary="Список КТС проекта"),
    retrieve=extend_schema(summary="Детали КТС проекта"),
    create=extend_schema(summary="Добавить КТС к проекту"),
    update=extend_schema(summary="Обновить КТС проекта"),
    partial_update=extend_schema(summary="Частичное обновление КТС проекта"),
    destroy=extend_schema(summary="Удалить КТС проекта"),
)
class ProjectKTSViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления КТС в рамках проекта.
    """

    serializer_class = ProjectKTSSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        project_id = self.kwargs.get('project_pk')
        if project_id:
            return ProjectKTS.objects.filter(project_id=project_id)
        return ProjectKTS.objects.all()

    def perform_create(self, serializer):
        project_id = self.kwargs.get('project_pk')
        if not project_id:
            raise ValidationError({'detail': 'project_pk is required in the URL.'})
        serializer.save(project_id=project_id)
