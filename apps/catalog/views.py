from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from .models import CatalogItem, CatalogUnit, CatalogKTS
from .serializers import (
    CatalogItemSerializer,
    CatalogUnitSerializer,
    CatalogKTSSerializer,
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
)
class CatalogItemViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CatalogItem.objects.all()
    permission_classes = [AllowAny]
    serializer_class = CatalogItemSerializer


@extend_schema_view(
    list=extend_schema(
        summary="Получить список юнитов",
        description="Возвращает список всех юнитов с вложенными изделиями."
    ),
    retrieve=extend_schema(
        summary="Получить юнит",
        description="Возвращает подробную информацию о юните с изделиями по ID."
    ),
)
class CatalogUnitViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CatalogUnit.objects.all()
    permission_classes = [AllowAny]
    serializer_class = CatalogUnitSerializer


@extend_schema_view(
    list=extend_schema(
        summary="Получить список КТС",
        description="Возвращает список всех КТС с вложенными юнитами и изделиями."
    ),
    retrieve=extend_schema(
        summary="Получить КТС",
        description="Возвращает подробную информацию о КТС по ID."
    ),
)
class CatalogKTSViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CatalogKTS.objects.all()
    permission_classes = [AllowAny]
    serializer_class = CatalogKTSSerializer