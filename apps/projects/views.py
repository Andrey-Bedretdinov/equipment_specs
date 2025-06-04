from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny

from .models import Project
from .serializers import ProjectSerializer, ProjectShortSerializer


@extend_schema_view(
    list=extend_schema(
        summary="Получить список проектов с вложенными данными",
        description=(
            "Возвращает полный список проектов.\n\n"
            "Каждый проект включает вложенные сущности:\n"
            "- КТС с вложенными юнитами и изделиями\n"
            "- Юниты с вложенными изделиями\n"
            "- Изделия, напрямую добавленные в проект\n\n"
            "Позволяет получить всю иерархию проекта в одном запросе."
        )
    ),
    retrieve=extend_schema(
        summary="Получить подробную информацию о проекте",
        description=(
            "Возвращает детальную информацию о проекте по его ID.\n\n"
            "Структура включает вложенные КТС, юниты и изделия проекта.\n"
            "Полезно для отображения полной спецификации одного проекта."
        )
    ),
)
class ProjectViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Вьюсет для работы с проектами.

    Доступные операции:
    - list: получить список всех проектов с вложенными данными (КТС, юниты, изделия)
    - retrieve: получить подробную информацию об одном проекте по ID
    """

    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [AllowAny]


@extend_schema(
    summary="Получить упрощённый список проектов",
    description=(
        "Возвращает краткую информацию о всех проектах без вложенных сущностей.\n\n"
        "Только основные данные:\n"
        "- ID проекта\n"
        "- Наименование\n"
        "- Описание\n"
        "- Итоговая стоимость проекта\n\n"
        "Полезно для списков, выборок и фильтрации проектов без лишних вложений."
    ),
    responses={200: ProjectShortSerializer(many=True)}
)
class ProjectShortListView(ListAPIView):
    """
    Список проектов без вложенных сущностей.

    Доступные данные:
    - ID проекта
    - Название проекта
    - Описание проекта
    - Итоговая стоимость проекта
    """

    queryset = Project.objects.all()
    serializer_class = ProjectShortSerializer
    permission_classes = [AllowAny]