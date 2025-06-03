from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter

from apps.catalog.views import CatalogItemViewSet, CatalogUnitViewSet, CatalogKTSViewSet
from apps.items.views import ProjectItemViewSet
from apps.kts.views import ProjectKTSViewSet
from apps.projects.views import ProjectViewSet
from apps.units.views import ProjectUnitViewSet

# основной роутер
router = DefaultRouter()
router.register(r'projects', ProjectViewSet, basename='projects')

# вложенный роутер для project -> kts
projects_router = NestedDefaultRouter(router, r'projects', lookup='project')
projects_router.register(r'kts', ProjectKTSViewSet, basename='project-kts')

# вложенный роутер для project_kts -> units
kts_router = NestedDefaultRouter(projects_router, r'kts', lookup='project_kts')
kts_router.register(r'units', ProjectUnitViewSet, basename='kts-units')

# вложенный роутер для project_unit -> items
units_router = NestedDefaultRouter(kts_router, r'units', lookup='project_unit')
units_router.register(r'items', ProjectItemViewSet, basename='unit-items')

# роутер для справочника
catalog_router = DefaultRouter()
catalog_router.register(r'catalog/items', CatalogItemViewSet, basename='catalog-items')
catalog_router.register(r'catalog/units', CatalogUnitViewSet, basename='catalog-units')
catalog_router.register(r'catalog/kts', CatalogKTSViewSet, basename='catalog-kts')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/', include(projects_router.urls)),
    path('api/', include(kts_router.urls)),
    path('api/', include(units_router.urls)),
    path('api/', include(catalog_router.urls)),

    # schema
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/docs/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]