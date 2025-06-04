from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import ProjectViewSet, ProjectShortListView

router = DefaultRouter()
router.register(r'projects', ProjectViewSet, basename='projects')

urlpatterns = [
    path('projects/short/', ProjectShortListView.as_view(), name='projects-short-list'),
]

urlpatterns += router.urls
