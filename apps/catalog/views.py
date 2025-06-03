from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import CatalogItem, CatalogUnit, CatalogKTS
from .serializers import CatalogItemSerializer, CatalogUnitSerializer, CatalogKTSSerializer


@extend_schema_view(
    list=extend_schema(summary="Список изделий справочника"),
    retrieve=extend_schema(summary="Детали изделия справочника"),
    create=extend_schema(summary="Создать изделие справочника"),
    update=extend_schema(summary="Обновить изделие справочника"),
    partial_update=extend_schema(summary="Частичное обновление изделия справочника"),
    destroy=extend_schema(summary="Удалить изделие справочника"),
)
class CatalogItemViewSet(viewsets.ModelViewSet):
    queryset = CatalogItem.objects.all()
    serializer_class = CatalogItemSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


@extend_schema_view(
    list=extend_schema(summary="Список комплектных единиц справочника"),
    retrieve=extend_schema(summary="Детали комплектной единицы справочника"),
    create=extend_schema(summary="Создать комплектную единицу справочника"),
    update=extend_schema(summary="Обновить комплектную единицу справочника"),
    partial_update=extend_schema(summary="Частичное обновление комплектной единицы справочника"),
    destroy=extend_schema(summary="Удалить комплектную единицу справочника"),
)
class CatalogUnitViewSet(viewsets.ModelViewSet):
    queryset = CatalogUnit.objects.all()
    serializer_class = CatalogUnitSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


@extend_schema_view(
    list=extend_schema(summary="Список КТС справочника"),
    retrieve=extend_schema(summary="Детали КТС справочника"),
    create=extend_schema(summary="Создать КТС справочника"),
    update=extend_schema(summary="Обновить КТС справочника"),
    partial_update=extend_schema(summary="Частичное обновление КТС справочника"),
    destroy=extend_schema(summary="Удалить КТС справочника"),
)
class CatalogKTSViewSet(viewsets.ModelViewSet):
    queryset = CatalogKTS.objects.all()
    serializer_class = CatalogKTSSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
