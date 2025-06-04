# apps/catalog/api_catalog_edit.py

from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import (
    CatalogItem, CatalogUnit, CatalogUnitItem, CatalogKTS, CatalogKTSUnit, CatalogKTSItem
)


class CatalogItemAPIView(APIView):
    """
    POST — создать изделие
    PATCH — изменить изделие
    DELETE — удалить изделие
    """

    @extend_schema(
        request={
            'application/json': {
                'type': 'object',
                'properties': {
                    'name': {'type': 'string'},
                    'description': {'type': 'string'},
                    'supplier': {'type': 'string'},
                    'catalog_code': {'type': 'string'},
                    'price': {'type': 'string'},
                    'currency': {'type': 'string'},
                    'manufactured': {'type': 'string'},
                    'delivery_type': {'type': 'string'}
                },
                'required': ['name', 'supplier', 'catalog_code', 'price', 'currency']
            }
        },
        responses={201: None}
    )
    def post(self, request):
        """Создать изделие"""
        data = request.data
        item = CatalogItem.objects.create(**data)
        return Response({'id': item.id}, status=status.HTTP_201_CREATED)

    @extend_schema(
        request={
            'application/json': {
                'type': 'object',
                'properties': {
                    'id': {'type': 'integer'},
                    'name': {'type': 'string'},
                    'description': {'type': 'string'},
                    'supplier': {'type': 'string'},
                    'catalog_code': {'type': 'string'},
                    'price': {'type': 'string'},
                    'currency': {'type': 'string'},
                    'manufactured': {'type': 'string'},
                    'delivery_type': {'type': 'string'}
                },
                'required': ['id']
            }
        },
        responses={200: None}
    )
    def patch(self, request):
        """Изменить изделие"""
        data = request.data
        try:
            item = CatalogItem.objects.get(id=data['id'])
        except CatalogItem.DoesNotExist:
            return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)

        for field, value in data.items():
            if field != 'id':
                setattr(item, field, value)
        item.save()
        return Response({'id': item.id}, status=status.HTTP_200_OK)

    @extend_schema(
        request={
            'application/json': {
                'type': 'object',
                'properties': {
                    'id': {'type': 'integer'}
                },
                'required': ['id']
            }
        },
        responses={204: None}
    )
    def delete(self, request):
        """Удалить изделие"""
        item_id = request.data.get('id')
        CatalogItem.objects.filter(id=item_id).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CatalogUnitAPIView(APIView):
    """
    POST — создать юнит
    PATCH — изменить юнит или добавить изделия
    DELETE — удалить юнит
    """

    @extend_schema(
        request={
            'application/json': {
                'type': 'object',
                'properties': {
                    'name': {'type': 'string'},
                    'description': {'type': 'string'}
                },
                'required': ['name']
            }
        },
        responses={201: None}
    )
    def post(self, request):
        """Создать пустой юнит"""
        data = request.data
        unit = CatalogUnit.objects.create(**data)
        return Response({'id': unit.id}, status=status.HTTP_201_CREATED)

    @extend_schema(
        request={
            'application/json': {
                'type': 'object',
                'properties': {
                    'id': {'type': 'integer'},
                    'name': {'type': 'string'},
                    'description': {'type': 'string'},
                    'items': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'item_id': {'type': 'integer'},
                                'quantity': {'type': 'integer'}
                            }
                        }
                    }
                },
                'required': ['id']
            }
        },
        responses={200: None}
    )
    def patch(self, request):
        """Изменить юнит или добавить изделия"""
        data = request.data
        try:
            unit = CatalogUnit.objects.get(id=data['id'])
        except CatalogUnit.DoesNotExist:
            return Response({"error": "Unit not found"}, status=status.HTTP_404_NOT_FOUND)

        if 'name' in data:
            unit.name = data['name']
        if 'description' in data:
            unit.description = data['description']
        unit.save()

        if 'items' in data:
            for item in data['items']:
                CatalogUnitItem.objects.create(
                    unit=unit,
                    item_id=item['item_id'],
                    quantity=item['quantity']
                )

        return Response({'id': unit.id}, status=status.HTTP_200_OK)

    @extend_schema(
        request={
            'application/json': {
                'type': 'object',
                'properties': {
                    'id': {'type': 'integer'}
                },
                'required': ['id']
            }
        },
        responses={204: None}
    )
    def delete(self, request):
        """Удалить юнит"""
        unit_id = request.data.get('id')
        CatalogUnit.objects.filter(id=unit_id).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CatalogKTSAPIView(APIView):
    """
    POST — создать ктс
    PATCH — изменить ктс или добавить юниты и изделия
    DELETE — удалить ктс
    """

    @extend_schema(
        request={
            'application/json': {
                'type': 'object',
                'properties': {
                    'name': {'type': 'string'},
                    'description': {'type': 'string'}
                },
                'required': ['name']
            }
        },
        responses={201: None}
    )
    def post(self, request):
        """Создать пустой КТС"""
        data = request.data
        kts = CatalogKTS.objects.create(**data)
        return Response({'id': kts.id}, status=status.HTTP_201_CREATED)

    @extend_schema(
        request={
            'application/json': {
                'type': 'object',
                'properties': {
                    'id': {'type': 'integer'},
                    'name': {'type': 'string'},
                    'description': {'type': 'string'},
                    'units': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'unit_id': {'type': 'integer'},
                                'quantity': {'type': 'integer'}
                            }
                        }
                    },
                    'items': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'item_id': {'type': 'integer'},
                                'quantity': {'type': 'integer'}
                            }
                        }
                    }
                },
                'required': ['id']
            }
        },
        responses={200: None}
    )
    def patch(self, request):
        """Изменить КТС или добавить юниты и изделия"""
        data = request.data
        try:
            kts = CatalogKTS.objects.get(id=data['id'])
        except CatalogKTS.DoesNotExist:
            return Response({"error": "KTS not found"}, status=status.HTTP_404_NOT_FOUND)

        if 'name' in data:
            kts.name = data['name']
        if 'description' in data:
            kts.description = data['description']
        kts.save()

        if 'units' in data:
            for unit in data['units']:
                CatalogKTSUnit.objects.create(
                    kts=kts,
                    unit_id=unit['unit_id'],
                    quantity=unit['quantity']
                )

        if 'items' in data:
            for item in data['items']:
                CatalogKTSItem.objects.create(
                    kts=kts,
                    item_id=item['item_id'],
                    quantity=item['quantity']
                )

        return Response({'id': kts.id}, status=status.HTTP_200_OK)

    @extend_schema(
        request={
            'application/json': {
                'type': 'object',
                'properties': {
                    'id': {'type': 'integer'}
                },
                'required': ['id']
            }
        },
        responses={204: None}
    )
    def delete(self, request):
        """Удалить КТС"""
        kts_id = request.data.get('id')
        CatalogKTS.objects.filter(id=kts_id).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
