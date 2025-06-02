from rest_framework_nested import routers

from apps.items.views import ItemViewSet
from apps.kts.views import KTSViewSet
from apps.projects.views import ProjectViewSet
from apps.units.views import UnitViewSet

# основной роутер
router = routers.DefaultRouter()
router.register(r'projects', ProjectViewSet, basename='project')
router.register(r'kts', KTSViewSet, basename='kts')
router.register(r'units', UnitViewSet, basename='unit')
router.register(r'items', ItemViewSet, basename='item')

# вложенные роутеры
projects_router = routers.NestedDefaultRouter(router, r'projects', lookup='project')
projects_router.register(r'kts', KTSViewSet, basename='project-kts')

kts_router = routers.NestedDefaultRouter(router, r'kts', lookup='kts')
kts_router.register(r'units', UnitViewSet, basename='kts-units')

units_router = routers.NestedDefaultRouter(router, r'units', lookup='unit')
units_router.register(r'items', ItemViewSet, basename='unit-items')

urlpatterns = router.urls + projects_router.urls + kts_router.urls + units_router.urls
