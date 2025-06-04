from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets, mixins
from rest_framework.permissions import AllowAny

from .models import CatalogItem, CatalogUnit, CatalogKTS
from .serializers import (
    CatalogItemSerializer, CatalogItemCreateSerializer,
    CatalogUnitSerializer,
    CatalogKTSSerializer, CatalogUnitCreateUpdateSerializer,
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
        request=CatalogItemCreateSerializer,
        responses={201: CatalogItemSerializer},
    ),
)
class CatalogItemViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,  # <-- Добавляем только create
    viewsets.GenericViewSet
):
    queryset = CatalogItem.objects.all()
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        if self.action == 'create':
            return CatalogItemCreateSerializer
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
)
class CatalogUnitViewSet(viewsets.ModelViewSet):
    queryset = CatalogUnit.objects.all()
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        if self.action in ['create']:
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
)
class CatalogKTSViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CatalogKTS.objects.all()
    permission_classes = [AllowAny]
    serializer_class = CatalogKTSSerializer