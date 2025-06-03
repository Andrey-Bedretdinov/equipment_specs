from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import CatalogItemViewSet, CatalogUnitViewSet, CatalogKTSViewSet

router = DefaultRouter()
router.register(r'items', CatalogItemViewSet, basename='catalog-items')
router.register(r'units', CatalogUnitViewSet, basename='catalog-units')
router.register(r'kts', CatalogKTSViewSet, basename='catalog-kts')

urlpatterns = [
    path('', include(router.urls)),
]
