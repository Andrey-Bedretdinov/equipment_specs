from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Project
from .serializers import ProjectSerializer


@extend_schema_view(
    list=extend_schema(summary="Список проектов пользователя"),
    retrieve=extend_schema(summary="Детали проекта"),
    create=extend_schema(summary="Создать новый проект"),
    update=extend_schema(summary="Обновить проект"),
    partial_update=extend_schema(summary="Частичное обновление проекта"),
    destroy=extend_schema(summary="Удалить проект"),
)
class ProjectViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления проектами.

    Доступные операции:
    - получить список проектов
    - получить информацию о проекте
    - создать проект
    - изменить проект
    - удалить проект
    """

    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Project.objects.filter(created_by=self.request.user)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)