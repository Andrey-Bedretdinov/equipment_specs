# apps/catalog/urls.py
from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import CatalogItemViewSet, CatalogUnitViewSet, CatalogKTSViewSet
from .api_catalog_edit import CatalogItemAPIView, CatalogUnitAPIView, CatalogKTSAPIView

router = DefaultRouter()
router.register(r'catalog/items', CatalogItemViewSet, basename='catalog-items')
router.register(r'catalog/units', CatalogUnitViewSet, basename='catalog-units')
router.register(r'catalog/kts', CatalogKTSViewSet, basename='catalog-kts')

urlpatterns = router.urls + [  # <-- Сначала роутер!
    path('catalog/items/edit/', CatalogItemAPIView.as_view(), name='catalog-item-edit'),
    path('catalog/units/edit/', CatalogUnitAPIView.as_view(), name='catalog-unit-edit'),
    path('catalog/kts/edit/', CatalogKTSAPIView.as_view(), name='catalog-kts-edit'),
]