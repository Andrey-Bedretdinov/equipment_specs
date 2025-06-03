from rest_framework.routers import DefaultRouter
from .views import ProjectUnitViewSet

router = DefaultRouter()
router.register(r'units', ProjectUnitViewSet, basename='units')

urlpatterns = router.urls
