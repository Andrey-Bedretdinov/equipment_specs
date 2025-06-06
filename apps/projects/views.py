from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets, status, mixins
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import Project
from .serializers import ProjectSerializer, ProjectShortSerializer, ProjectCreateSerializer


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
@extend_schema_view(
    list=extend_schema(summary="Список проектов (полный)"),
    retrieve=extend_schema(summary="Получить проект"),
    create=extend_schema(
        summary="Создать пустой проект",
        request=ProjectCreateSerializer,
        responses={201: ProjectSerializer},
    ),
    destroy=extend_schema(
        summary="Удалить проект",
        responses={204: None},
    ),
)
class ProjectViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,  # ← добавили
    mixins.DestroyModelMixin,  # ← добавили
    viewsets.GenericViewSet,
):
    queryset = Project.objects.all()
    permission_classes = [AllowAny]

    # выбор сериализатора
    def get_serializer_class(self):
        if self.action == "create":
            return ProjectCreateSerializer
        return ProjectSerializer

    # переопределяем create, чтобы вернуть «read»-сериализатор с id
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        read_serializer = ProjectSerializer(serializer.instance, context=self.get_serializer_context())
        headers = self.get_success_headers(read_serializer.data)
        return Response(read_serializer.data, status=status.HTTP_201_CREATED, headers=headers)


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