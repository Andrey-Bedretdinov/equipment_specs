from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import viewsets
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.permissions import IsAuthenticated

from apps.projects.models import Project
from .models import KTS
from .serializers import KTSSerializer


@extend_schema_view(
    list=extend_schema(description="Получить список всех КТС проекта."),
    retrieve=extend_schema(description="Получить детали КТС."),
    create=extend_schema(description="Создать новый КТС для проекта."),
    update=extend_schema(description="Обновить КТС."),
    destroy=extend_schema(description="Удалить КТС."),
)
class KTSViewSet(viewsets.ModelViewSet):
    """
    Управление комплексами технических средств (КТС).
    """
    queryset = KTS.objects.all()
    serializer_class = KTSSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if 'project_pk' in self.kwargs:
            return self.queryset.filter(project_id=self.kwargs['project_pk'])
        return super().get_queryset()

    def perform_create(self, serializer):
        project_id = self.kwargs.get('project_pk')
        if project_id:
            try:
                project = Project.objects.get(pk=project_id)
            except Project.DoesNotExist:
                raise NotFound('Project not found')
            serializer.save(project=project)
        else:
            raise ValidationError('Project id is required')
