from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import KTSViewSet

router = DefaultRouter()
router.register(r'kts', KTSViewSet, basename='kts-detail')  # для операций с конкретным КТС

urlpatterns = [
    path('projects/<int:project_id>/kts/', KTSViewSet.as_view({'post': 'create', 'get': 'list'}), name='project-kts'),
]

urlpatterns += router.urls
