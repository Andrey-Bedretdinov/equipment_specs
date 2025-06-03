from rest_framework.routers import DefaultRouter
from .views import ProjectViewSet
from django.urls import path
from .views import ProjectFullTreeView

router = DefaultRouter()
router.register(r'projects', ProjectViewSet, basename='projects')

urlpatterns = router.urls

urlpatterns += [
    path('projects/full_tree/', ProjectFullTreeView.as_view(), name='projects-full-tree'),
]