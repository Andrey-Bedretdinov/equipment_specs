from rest_framework.routers import DefaultRouter
from .views import ProjectKTSViewSet

router = DefaultRouter()
router.register(r'kts', ProjectKTSViewSet, basename='kts')

urlpatterns = router.urls
