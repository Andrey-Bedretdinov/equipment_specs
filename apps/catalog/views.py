from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from .models import CatalogItem, CatalogUnit, CatalogKTS
from .serializers import (
    CatalogItemSerializer,
    CatalogUnitSerializer,
    CatalogKTSSerializer
)


class CatalogItemViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CatalogItem.objects.all()
    serializer_class = CatalogItemSerializer
    permission_classes = [AllowAny]


class CatalogUnitViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CatalogUnit.objects.all()
    serializer_class = CatalogUnitSerializer
    permission_classes = [AllowAny]


class CatalogKTSViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CatalogKTS.objects.all()
    serializer_class = CatalogKTSSerializer
    permission_classes = [AllowAny]
