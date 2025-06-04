from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from .models import CatalogItem, CatalogUnit, CatalogKTS
from .serializers import (
    CatalogItemSerializer, CatalogItemCreateUpdateSerializer,
    CatalogUnitSerializer, CatalogUnitCreateUpdateSerializer,
    CatalogKTSSerializer, CatalogKTSCreateUpdateSerializer
)


class CatalogItemViewSet(viewsets.ModelViewSet):
    queryset = CatalogItem.objects.all()
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return CatalogItemCreateUpdateSerializer
        return CatalogItemSerializer

    @extend_schema(
        request=CatalogItemCreateUpdateSerializer,
        responses={201: CatalogItemSerializer}
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
        request=CatalogItemCreateUpdateSerializer,
        responses={200: CatalogItemSerializer}
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @extend_schema(
        request=CatalogItemCreateUpdateSerializer,
        responses={200: CatalogItemSerializer}
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @extend_schema(
        responses={204: None}
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class CatalogUnitViewSet(viewsets.ModelViewSet):
    queryset = CatalogUnit.objects.all()
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return CatalogUnitCreateUpdateSerializer
        return CatalogUnitSerializer

    @extend_schema(
        request=CatalogUnitCreateUpdateSerializer,
        responses={201: CatalogUnitSerializer}
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
        request=CatalogUnitCreateUpdateSerializer,
        responses={200: CatalogUnitSerializer}
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @extend_schema(
        request=CatalogUnitCreateUpdateSerializer,
        responses={200: CatalogUnitSerializer}
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @extend_schema(
        responses={204: None}
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class CatalogKTSViewSet(viewsets.ModelViewSet):
    queryset = CatalogKTS.objects.all()
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return CatalogKTSCreateUpdateSerializer
        return CatalogKTSSerializer

    @extend_schema(
        request=CatalogKTSCreateUpdateSerializer,
        responses={201: CatalogKTSSerializer}
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
        request=CatalogKTSCreateUpdateSerializer,
        responses={200: CatalogKTSSerializer}
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @extend_schema(
        request=CatalogKTSCreateUpdateSerializer,
        responses={200: CatalogKTSSerializer}
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @extend_schema(
        responses={204: None}
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
