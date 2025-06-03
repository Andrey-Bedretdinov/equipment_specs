from rest_framework.routers import DefaultRouter

from .views import ProjectItemViewSet

router = DefaultRouter()
router.register(r'items', ProjectItemViewSet, basename='items')

urlpatterns = router.urls
