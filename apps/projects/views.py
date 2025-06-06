from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets, status, mixins
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import Project, ProjectItem, ProjectUnit, ProjectKTS
from .serializers import ProjectSerializer, ProjectShortSerializer, ProjectCreateSerializer, ProjectElementsSerializer
from ..catalog.models import CatalogItem, CatalogUnit, CatalogKTS


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

    # ——— POST /projects/{id}/  →  «ADD» ———
    @extend_schema(
        summary="Добавить объекты в проект",
        request=ProjectElementsSerializer,
        responses={200: ProjectSerializer},
        methods=["POST"],
    )
    def post(self, request, pk=None, *args, **kwargs):
        project = self.get_object()
        ser = ProjectElementsSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        v = ser.validated_data

        for obj in v.get("items", []):
            ProjectItem.objects.create(
                project=project,
                item=CatalogItem.objects.get(id=obj["item_id"]),
                quantity=obj.get("quantity", 1),
            )

        for obj in v.get("units", []):
            ProjectUnit.objects.create(
                project=project,
                unit=CatalogUnit.objects.get(id=obj["unit_id"]),
                quantity=obj.get("quantity", 1),
            )

        for obj in v.get("kts", []):
            ProjectKTS.objects.create(
                project=project,
                kts=CatalogKTS.objects.get(id=obj["kts_id"]),
                quantity=obj.get("quantity", 1),
            )

        return Response(ProjectSerializer(project).data)

    # ——— PATCH /projects/{id}/  →  «UPDATE quantity» ———
    @extend_schema(
        summary="Изменить количество объектов в проекте",
        request=ProjectElementsSerializer,
        responses={200: ProjectSerializer},
        methods=["PATCH"],
    )
    def patch(self, request, pk=None, *args, **kwargs):
        project = self.get_object()
        ser = ProjectElementsSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        v = ser.validated_data

        def _update(qs, id_field, obj_key):
            for o in v.get(obj_key, []):
                inst = qs.get(**{id_field: o[f"{obj_key[:-1]}_id"]})
                inst.quantity = o["quantity"]
                inst.save()

        _update(ProjectItem.objects.filter(project=project), "item_id", "items")
        _update(ProjectUnit.objects.filter(project=project), "unit_id", "units")
        _update(ProjectKTS.objects.filter(project=project), "kts_id", "kts")

        return Response(ProjectSerializer(project).data)

    # ---------- PUT  /projects/{id}/  → удалить элементы ----------
    @extend_schema(
        summary="Удалить указанные элементы из проекта",
        request=ProjectElementsSerializer,
        responses={200: ProjectSerializer},
        methods=["PUT"],
    )
    def put(self, request, pk=None, *args, **kwargs):
        project = self.get_object()
        ser = ProjectElementsSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        v = ser.validated_data

        # items
        if "items" in v:
            ids = [o["item_id"] for o in v["items"]]
            ProjectItem.objects.filter(project=project, item_id__in=ids).delete()

        # units
        if "units" in v:
            ids = [o["unit_id"] for o in v["units"]]
            ProjectUnit.objects.filter(project=project, unit_id__in=ids).delete()

        # kts
        if "kts" in v:
            ids = [o["kts_id"] for o in v["kts"]]
            ProjectKTS.objects.filter(project=project, kts_id__in=ids).delete()

        return Response(ProjectSerializer(project).data)

    # ---------- DELETE  /projects/{id}/  → удалить проект ----------
    @extend_schema(
        summary="Удалить проект",
        request=ProjectElementsSerializer,
        responses={200: ProjectSerializer, 204: None},
        methods=["DELETE"],
    )
    def delete(self, request, pk=None, *args, **kwargs):
        project = self.get_object()
        self.perform_destroy(project)
        return Response(status=status.HTTP_204_NO_CONTENT)


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