from rest_framework import serializers

from .models import CatalogItem, CatalogUnit, CatalogUnitItem, CatalogKTS, CatalogKTSUnit, CatalogKTSItem


class CatalogItemSerializer(serializers.ModelSerializer):
    """
    Сериализатор для чтения информации об изделии.

    Отдаёт:
    - id: идентификатор изделия
    - name: наименование изделия
    - description: описание изделия
    - supplier: поставщик
    - catalog_code: артикул
    - price: цена за единицу
    - currency: валюта цены
    - manufactured: производитель
    - delivery_type: тип поставки (например, склад / под заказ)
    """

    class Meta:
        model = CatalogItem
        fields = [
            'id', 'name', 'description', 'supplier', 'catalog_code',
            'price', 'currency', 'manufactured', 'delivery_type'
        ]


class CatalogItemCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания и редактирования изделия.

    Используется для POST (создание) и PATCH (обновление) запросов.

    Поля:
    - name: наименование изделия (обязательное)
    - description: описание изделия (опционально)
    - supplier: поставщик
    - catalog_code: артикул
    - price: цена
    - currency: валюта
    - manufactured: производитель
    - delivery_type: тип поставки
    """

    class Meta:
        model = CatalogItem
        fields = [
            'id', 'name', 'description', 'supplier', 'catalog_code',
            'price', 'currency', 'manufactured', 'delivery_type'
        ]
        read_only_fields = ['id']


class CatalogUnitItemSerializer(serializers.ModelSerializer):
    """
    Сериализатор для изделия внутри юнита (read only).

    Отдаёт:
    - id: идентификатор связи
    - item: вложенный объект изделия
    - quantity: количество изделий в юните
    """
    item = CatalogItemSerializer(read_only=True)

    class Meta:
        model = CatalogUnitItem
        fields = ['id', 'item', 'quantity']


class CatalogUnitItemCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания / обновления изделия в юните.

    Используется для:
    - unit: ID юнита
    - item: ID изделия
    - quantity: количество
    """

    class Meta:
        model = CatalogUnitItem
        fields = ['id', 'unit', 'item', 'quantity']
        read_only_fields = ['id']


class CatalogUnitSerializer(serializers.ModelSerializer):
    """
    Сериализатор для чтения информации о юните.

    Отдаёт:
    - id: идентификатор юнита
    - name: наименование юнита
    - description: описание
    - items: список изделий в юните
    """
    items = serializers.SerializerMethodField()

    class Meta:
        model = CatalogUnit
        fields = ['id', 'name', 'description', 'items']

    def get_items(self, obj):
        """
        Возвращает список изделий, входящих в юнит.
        """
        unit_items = CatalogUnitItem.objects.filter(unit=obj)
        return CatalogUnitItemSerializer(unit_items, many=True).data


class CatalogUnitCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания и редактирования юнита.

    Используется для POST и PATCH.

    Поля:
    - name: наименование
    - description: описание
    """

    class Meta:
        model = CatalogUnit
        fields = ['id', 'name', 'description']
        read_only_fields = ['id']


class CatalogKTSUnitSerializer(serializers.ModelSerializer):
    """
    Сериализатор для чтения юнита внутри КТС.

    Отдаёт:
    - id: идентификатор связи
    - unit: вложенный юнит
    - quantity: количество юнитов
    """
    unit = CatalogUnitSerializer(read_only=True)

    class Meta:
        model = CatalogKTSUnit
        fields = ['id', 'unit', 'quantity']


class CatalogKTSUnitCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания и редактирования связи КТС-Юнит.

    Используется для:
    - kts: ID КТС
    - unit: ID юнита
    - quantity: количество
    """

    class Meta:
        model = CatalogKTSUnit
        fields = ['id', 'kts', 'unit', 'quantity']
        read_only_fields = ['id']


class CatalogKTSItemSerializer(serializers.ModelSerializer):
    """
    Сериализатор для чтения изделия внутри КТС.

    Отдаёт:
    - id: идентификатор связи
    - item: вложенный объект изделия
    - quantity: количество изделий
    """
    item = CatalogItemSerializer(read_only=True)

    class Meta:
        model = CatalogKTSItem
        fields = ['id', 'item', 'quantity']


class CatalogKTSItemCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания и редактирования связи КТС-Изделие.

    Используется для:
    - kts: ID КТС
    - item: ID изделия
    - quantity: количество
    """

    class Meta:
        model = CatalogKTSItem
        fields = ['id', 'kts', 'item', 'quantity']
        read_only_fields = ['id']


class CatalogKTSSerializer(serializers.ModelSerializer):
    """
    Сериализатор для чтения информации о КТС.

    Отдаёт:
    - id: идентификатор КТС
    - name: наименование
    - description: описание
    - units: список юнитов с количеством
    - items: список изделий с количеством
    """
    units = serializers.SerializerMethodField()
    items = serializers.SerializerMethodField()

    class Meta:
        model = CatalogKTS
        fields = ['id', 'name', 'description', 'units', 'items']

    def get_units(self, obj):
        """
        Возвращает список юнитов внутри КТС.
        """
        kts_units = CatalogKTSUnit.objects.filter(kts=obj)
        return CatalogKTSUnitSerializer(kts_units, many=True).data

    def get_items(self, obj):
        """
        Возвращает список изделий внутри КТС.
        """
        kts_items = CatalogKTSItem.objects.filter(kts=obj)
        return CatalogKTSItemSerializer(kts_items, many=True).data


class CatalogKTSCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания и редактирования КТС.

    Используется для POST и PATCH.

    Поля:
    - name: наименование
    - description: описание
    """

    class Meta:
        model = CatalogKTS
        fields = ['id', 'name', 'description']
        read_only_fields = ['id']