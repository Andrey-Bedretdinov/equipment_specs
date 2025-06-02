from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import ItemViewSet

router = DefaultRouter()
router.register(r'items', ItemViewSet, basename='item-detail')  # для операций с конкретным изделием

urlpatterns = [
    path('units/<int:unit_id>/items/', ItemViewSet.as_view({'post': 'create', 'get': 'list'}), name='unit-items'),
]

urlpatterns += router.urls
