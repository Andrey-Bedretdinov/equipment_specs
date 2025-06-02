from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import UnitViewSet

router = DefaultRouter()
router.register(r'units', UnitViewSet, basename='unit-detail')  # для операций с конкретной комплектной единицей

urlpatterns = [
    path('kts/<int:kts_id>/units/', UnitViewSet.as_view({'post': 'create', 'get': 'list'}), name='kts-units'),
]

urlpatterns += router.urls
