from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import CatalogItem, CatalogUnit, CatalogKTS, CatalogUnitItem, CatalogKTSItem, CatalogKTSUnit
from .serializers import (
    CatalogItemSerializer, CatalogItemCreateSerializer,
    CatalogUnitSerializer,
    CatalogKTSSerializer, CatalogUnitCreateUpdateSerializer, AddItemsToUnitSerializer, CatalogUnitItemSerializer,
    CatalogKTSCreateSerializer, AddElementsToKTSSerializer, CatalogKTSItemSerializer, CatalogKTSUnitSerializer,
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
    destroy=extend_schema(
        summary="Удалить изделие",
        description="Удаляет изделие и его связи из каталога.",
        responses={204: None},
    ),
)
class CatalogItemViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,  # <-- Добавляем только create
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    queryset = CatalogItem.objects.all()
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        if self.action == 'create':
            return CatalogItemCreateSerializer
        return CatalogItemSerializer

    def create(self, request, *args, **kwargs):
        """
        Переопределяем, чтобы  в ответе
        вернуть **читаемый** сериализатор с id.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        # пересериализуем сохранённый объект
        read_serializer = CatalogItemSerializer(serializer.instance)
        headers = self.get_success_headers(read_serializer.data)
        return Response(read_serializer.data, status=status.HTTP_201_CREATED, headers=headers)


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
    destroy=extend_schema(
        summary="Удалить юнит",
        description="Удаляет юнит и связанные записи (изделия внутри юнита, ссылки в КТС).",
        responses={204: None},
    ),
)
class CatalogUnitViewSet(mixins.ListModelMixin,
                         mixins.RetrieveModelMixin,
                         mixins.CreateModelMixin,  # <-- Добавляем только create
                         mixins.DestroyModelMixin,
                         viewsets.GenericViewSet):

    queryset = CatalogUnit.objects.all()
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        if self.action in ['create']:
            return CatalogUnitCreateUpdateSerializer
        return CatalogUnitSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        # «читаемый» сериализатор — уже с id
        read_serializer = CatalogUnitSerializer(serializer.instance)
        headers = self.get_success_headers(read_serializer.data)
        return Response(read_serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @extend_schema(
        request=AddItemsToUnitSerializer,
        responses={201: CatalogUnitItemSerializer(many=True)},
        summary="Добавить изделия в юнит",
        description="Добавляет новые изделия в юнит по ID юнита и списку изделий с количеством."
    )
    @action(detail=False, methods=['post'], url_path='add-items')
    def add_items(self, request):
        serializer = AddItemsToUnitSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        unit_id = serializer.validated_data['id']
        items_data = serializer.validated_data['items']

        # Проверка, существует ли юнит
        try:
            unit = CatalogUnit.objects.get(id=unit_id)
        except CatalogUnit.DoesNotExist:
            return Response({"error": "Юнит не найден."}, status=status.HTTP_404_NOT_FOUND)

        created_items = []
        for item_data in items_data:
            item_id = item_data['id']
            quantity = item_data.get('quantity', 1)

            try:
                item = CatalogItem.objects.get(id=item_id)
            except CatalogItem.DoesNotExist:
                return Response({"error": f"Изделие с id {item_id} не найдено."}, status=status.HTTP_404_NOT_FOUND)

            unit_item = CatalogUnitItem.objects.create(
                unit=unit,
                item=item,
                quantity=quantity
            )
            created_items.append(unit_item)

        # Возвращаем созданные связи
        return Response(CatalogUnitItemSerializer(created_items, many=True).data, status=status.HTTP_201_CREATED)


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
        request=CatalogKTSCreateSerializer,
        responses={201: CatalogKTSSerializer}
    ),
    destroy=extend_schema(
        summary="Удалить КТС",
        description="Удаляет КТС и все его связи (юниты и изделия).",
        responses={204: None},
    ),
)
class CatalogKTSViewSet(mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        mixins.CreateModelMixin,  # <-- Добавляем только create
                        mixins.DestroyModelMixin,
                        viewsets.GenericViewSet):

    queryset = CatalogKTS.objects.all()
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        if self.action == 'create':
            return CatalogKTSCreateSerializer
        return CatalogKTSSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        read_serializer = CatalogKTSSerializer(serializer.instance)
        headers = self.get_success_headers(read_serializer.data)
        return Response(read_serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @extend_schema(
        request=AddElementsToKTSSerializer,
        responses={201: CatalogKTSSerializer},
        summary="Добавить изделия и юниты в КТС",
        description=(
                "Позволяет единым запросом добавить изделия (items) и/или юниты (units) "
                "в существующий КТС. quantity по умолчанию = 1."
        )
    )
    @action(detail=False, methods=["post"], url_path="add-elements")
    def add_elements(self, request):
        serializer = AddElementsToKTSSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        kts_id = serializer.validated_data["kts_id"]
        items_data = serializer.validated_data.get("items", [])
        units_data = serializer.validated_data.get("units", [])

        # проверяем наличие ктс
        try:
            kts = CatalogKTS.objects.get(id=kts_id)
        except CatalogKTS.DoesNotExist:
            return Response({"error": "ктс не найден"}, status=status.HTTP_404_NOT_FOUND)

        # добавляем изделия
        created_items = []
        for item in items_data:
            item_id = item.get("item_id")
            qty = item.get("quantity", 1)
            try:
                obj = CatalogItem.objects.get(id=item_id)
            except CatalogItem.DoesNotExist:
                return Response({"error": f"изделие id {item_id} не найдено"}, status=status.HTTP_404_NOT_FOUND)
            created_items.append(
                CatalogKTSItem.objects.create(kts=kts, item=obj, quantity=qty)
            )

        # добавляем юниты
        created_units = []
        for unit in units_data:
            unit_id = unit.get("unit_id")
            qty = unit.get("quantity", 1)
            try:
                obj = CatalogUnit.objects.get(id=unit_id)
            except CatalogUnit.DoesNotExist:
                return Response({"error": f"юнит id {unit_id} не найден"}, status=status.HTTP_404_NOT_FOUND)
            created_units.append(
                CatalogKTSUnit.objects.create(kts=kts, unit=obj, quantity=qty)
            )

        # формируем ответ
        response = {
            "kts_id": kts.id,
            "items": CatalogKTSItemSerializer(created_items, many=True).data,
            "units": CatalogKTSUnitSerializer(created_units, many=True).data,
        }
        return Response(response, status=status.HTTP_201_CREATED)
