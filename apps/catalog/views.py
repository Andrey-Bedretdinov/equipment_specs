from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from .models import CatalogItem, CatalogUnit, CatalogKTS
from .serializers import (
    CatalogItemSerializer, CatalogItemCreateUpdateSerializer,
    CatalogUnitSerializer, CatalogUnitCreateUpdateSerializer,
    CatalogKTSSerializer, CatalogKTSCreateUpdateSerializer
)


@extend_schema_view(
    list=extend_schema(
        summary="Получить список изделий",
        description="Возвращает список всех изделий, доступных в каталоге."
    ),
    retrieve=extend_schema(
        summary="Получить изделие",
        description="Возвращает подробную информацию об одном изделии по ID."
    ),
    create=extend_schema(
        summary="Создать изделие",
        description="Создаёт новое изделие в каталоге.",
        request=CatalogItemCreateUpdateSerializer,
        responses={201: CatalogItemSerializer}
    ),
    update=extend_schema(
        summary="Обновить изделие (PUT)",
        description="Полностью обновляет изделие по ID.",
        request=CatalogItemCreateUpdateSerializer,
        responses={200: CatalogItemSerializer}
    ),
    partial_update=extend_schema(
        summary="Частично обновить изделие (PATCH)",
        description="Обновляет часть полей изделия по ID.",
        request=CatalogItemCreateUpdateSerializer,
        responses={200: CatalogItemSerializer}
    ),
    destroy=extend_schema(
        summary="Удалить изделие",
        description="Удаляет изделие из каталога по ID.",
        responses={204: None}
    ),
)
class CatalogItemViewSet(viewsets.ModelViewSet):
    queryset = CatalogItem.objects.all()
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return CatalogItemCreateUpdateSerializer
        return CatalogItemSerializer


@extend_schema_view(
    list=extend_schema(
        summary="Получить список юнитов",
        description="Возвращает список всех юнитов с вложенными изделиями."
    ),
    retrieve=extend_schema(
        summary="Получить юнит",
        description="Возвращает подробную информацию о юните с изделиями по ID."
    ),
    create=extend_schema(
        summary="Создать юнит",
        description="Создаёт новый юнит.",
        request=CatalogUnitCreateUpdateSerializer,
        responses={201: CatalogUnitSerializer}
    ),
    update=extend_schema(
        summary="Обновить юнит (PUT)",
        description="Полностью обновляет юнит по ID.",
        request=CatalogUnitCreateUpdateSerializer,
        responses={200: CatalogUnitSerializer}
    ),
    partial_update=extend_schema(
        summary="Частично обновить юнит (PATCH)",
        description="Обновляет часть полей юнита по ID.",
        request=CatalogUnitCreateUpdateSerializer,
        responses={200: CatalogUnitSerializer}
    ),
    destroy=extend_schema(
        summary="Удалить юнит",
        description="Удаляет юнит из каталога по ID.",
        responses={204: None}
    ),
)
class CatalogUnitViewSet(viewsets.ModelViewSet):
    queryset = CatalogUnit.objects.all()
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return CatalogUnitCreateUpdateSerializer
        return CatalogUnitSerializer


@extend_schema_view(
    list=extend_schema(
        summary="Получить список КТС",
        description="Возвращает список всех КТС с вложенными юнитами и изделиями."
    ),
    retrieve=extend_schema(
        summary="Получить КТС",
        description="Возвращает подробную информацию о КТС по ID."
    ),
    create=extend_schema(
        summary="Создать КТС",
        description="Создаёт новый КТС.",
        request=CatalogKTSCreateUpdateSerializer,
        responses={201: CatalogKTSSerializer}
    ),
    update=extend_schema(
        summary="Обновить КТС (PUT)",
        description="Полностью обновляет КТС по ID.",
        request=CatalogKTSCreateUpdateSerializer,
        responses={200: CatalogKTSSerializer}
    ),
    partial_update=extend_schema(
        summary="Частично обновить КТС (PATCH)",
        description="Обновляет часть полей КТС по ID.",
        request=CatalogKTSCreateUpdateSerializer,
        responses={200: CatalogKTSSerializer}
    ),
    destroy=extend_schema(
        summary="Удалить КТС",
        description="Удаляет КТС из каталога по ID.",
        responses={204: None}
    ),
)
class CatalogKTSViewSet(viewsets.ModelViewSet):
    queryset = CatalogKTS.objects.all()
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return CatalogKTSCreateUpdateSerializer
        return CatalogKTSSerializer
