from rest_framework.routers import DefaultRouter

from .views import CatalogItemViewSet, CatalogUnitViewSet, CatalogKTSViewSet

router = DefaultRouter()
router.register(r'catalog/items', CatalogItemViewSet, basename='catalog-items')
router.register(r'catalog/units', CatalogUnitViewSet, basename='catalog-units')
router.register(r'catalog/kts', CatalogKTSViewSet, basename='catalog-kts')

urlpatterns = router.urls
