# apps/projects/views.py
"""
Вью-модуль для работы с проектами.

Маршруты (router создаёт их автоматически):

GET    /projects/            – список (полный)
POST   /projects/            – создать пустой проект
GET    /projects/{id}/       – получить проект
POST   /projects/{id}/       – добавить элементы                 ← кастомный @action
PATCH  /projects/{id}/       – изменить quantity у элементов
PUT    /projects/{id}/       – удалить элементы
DELETE /projects/{id}/       – удалить проект
GET    /projects/short/      – упрощённый список
"""
from __future__ import annotations

from django.db import transaction
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import mixins, viewsets, status
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from apps.catalog.models import CatalogItem, CatalogUnit, CatalogKTS
from .models import Project, ProjectItem, ProjectUnit, ProjectKTS
from .serializers import (
    ProjectSerializer,
    ProjectShortSerializer,
    ProjectCreateSerializer,
    ProjectElementsSerializer,
)


def _pk_key(key: str) -> str:
    """items → item_id ; units → unit_id ; kts → kts_id"""
    return "kts_id" if key == "kts" else f"{key[:-1]}_id"

# ------------------------ ProjectViewSet ------------------------ #
@extend_schema_view(
    list=extend_schema(summary="Получить список проектов"),
    retrieve=extend_schema(summary="Получить проект"),
    destroy=extend_schema(summary="Удалить проект", responses={204: None}),
)
class ProjectViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,     # POST  /projects/
    mixins.UpdateModelMixin,     # PUT & PATCH  /projects/{id}/
    mixins.DestroyModelMixin,    # DELETE /projects/{id}/
    viewsets.GenericViewSet,
):
    queryset = Project.objects.all()
    permission_classes = [AllowAny]
    http_method_names = ["get", "post", "patch", "put", "delete", "head", "options"]

    # ---------- выбор сериализатора ----------
    def get_serializer_class(self):
        if self.action == "create":
            return ProjectCreateSerializer
        if self.request.method in ("POST", "PATCH", "PUT") and self.action != "create":
            return ProjectElementsSerializer
        return ProjectSerializer

    # ---------- create: пустой проект ----------
    @extend_schema(summary="Создать пустой проект", responses={201: ProjectSerializer})
    @extend_schema(summary="Создать пустой проект", responses={201: ProjectSerializer})
    def create(self, request, *args, **kwargs):
        write_ser = self.get_serializer(data=request.data)
        write_ser.is_valid(raise_exception=True)
        self.perform_create(write_ser)

        read_ser = ProjectSerializer(write_ser.instance, context=self.get_serializer_context())
        headers = self.get_success_headers(read_ser.data)
        return Response(read_ser.data, status=status.HTTP_201_CREATED, headers=headers)

    # ---------- POST /projects/{id}/ : добавить элементы ----------
    #   Кастомный detail-action с пустым url_path → конечный URL тот же /{id}/
    @extend_schema(summary="Добавить элементы в проект", responses={200: ProjectSerializer})
    @action(detail=True, methods=["post"], url_path="", url_name="add_elements")
    def add_elements(self, request, pk=None):
        project = self.get_object()
        data = self._validated_elements(request)

        with transaction.atomic():
            self._add_elements(project, data)

        return Response(ProjectSerializer(project).data)

    # ---------- PATCH /{id}/ : изменить количество ----------
    @extend_schema(summary="Изменить quantity", responses={200: ProjectSerializer})
    def partial_update(self, request, *args, **kwargs):
        project = self.get_object()
        data = self._validated_elements(request)

        with transaction.atomic():
            self._update_quantity(project, data)

        return Response(ProjectSerializer(project).data)

    # ---------- PUT /{id}/ : удалить элементы ----------
    @extend_schema(summary="Удалить элементы из проекта", responses={200: ProjectSerializer})
    def update(self, request, *args, **kwargs):
        project = self.get_object()
        data = self._validated_elements(request)

        with transaction.atomic():
            self._remove_elements(project, data)

        return Response(ProjectSerializer(project).data)

    # ---------- DELETE /{id}/ : удалить проект ----------
    # summary установлен в @extend_schema_view

    # ========== helpers ==========
    def _validated_elements(self, request):
        serializer = ProjectElementsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return serializer.validated_data

    def _add_elements(self, project: Project, data: dict) -> None:
        def _bulk(source_qs, model, key, link_field):
            id_field = _pk_key(key)
            objs = [
                model(
                    project=project,
                    **{link_field: get_object_or_404(source_qs, id=obj[id_field])},
                    quantity=obj.get("quantity", 1),
                )
                for obj in data.get(key, [])
            ]
            model.objects.bulk_create(objs)

        _bulk(CatalogItem.objects, ProjectItem, "items", "item")
        _bulk(CatalogUnit.objects, ProjectUnit, "units", "unit")
        _bulk(CatalogKTS.objects, ProjectKTS, "kts", "kts")

    def _update_quantity(self, project: Project, data: dict) -> None:
        def _apply(qs, key, id_field):
            id_key = _pk_key(key)
            for obj in data.get(key, []):
                qs.filter(**{id_field: obj[id_key]}).update(quantity=obj["quantity"])

        _apply(ProjectItem.objects.filter(project=project), "items", "item_id")
        _apply(ProjectUnit.objects.filter(project=project), "units", "unit_id")
        _apply(ProjectKTS.objects.filter(project=project), "kts", "kts_id")

    def _remove_elements(self, project: Project, data: dict) -> None:
        def _delete(qs, key, id_field):
            ids = [o[_pk_key(key)] for o in data.get(key, [])]
            if ids:
                qs.filter(**{f"{id_field}__in": ids}).delete()

        _delete(ProjectItem.objects.filter(project=project), "items", "item_id")
        _delete(ProjectUnit.objects.filter(project=project), "units", "unit_id")
        _delete(ProjectKTS.objects.filter(project=project), "kts", "kts_id")


# ------------------- ProjectShortListView ------------------- #
@extend_schema(
    summary="Получить упрощённый список проектов",
    responses={200: ProjectShortSerializer(many=True)},
)
class ProjectShortListView(ListAPIView):
    """Короткий список без вложенных сущностей."""
    queryset = Project.objects.all()
    serializer_class = ProjectShortSerializer
    permission_classes = [AllowAny]