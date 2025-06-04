from rest_framework import viewsets
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny

from .models import Project
from .serializers import ProjectSerializer, ProjectShortSerializer


class ProjectViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [AllowAny]


class ProjectShortListView(ListAPIView):
    """
    Возвращает список всех проектов без вложенных данных.
    """
    queryset = Project.objects.all()
    serializer_class = ProjectShortSerializer
