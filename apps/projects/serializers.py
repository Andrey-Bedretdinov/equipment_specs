from apps.catalog.serializers import CatalogItemSerializer, CatalogUnitSerializer, CatalogKTSSerializer
from rest_framework import serializers

from .models import Project, ProjectKTS, ProjectUnit, ProjectItem


class ProjectItemSerializer(serializers.ModelSerializer):
    item = CatalogItemSerializer(read_only=True)

    class Meta:
        model = ProjectItem
        fields = ['id', 'item', 'quantity']


class ProjectUnitSerializer(serializers.ModelSerializer):
    unit = CatalogUnitSerializer(read_only=True)

    class Meta:
        model = ProjectUnit
        fields = ['id', 'unit', 'quantity']


class ProjectKTSSerializer(serializers.ModelSerializer):
    kts = CatalogKTSSerializer(read_only=True)

    class Meta:
        model = ProjectKTS
        fields = ['id', 'kts', 'quantity']


class ProjectSerializer(serializers.ModelSerializer):
    kts_list = serializers.SerializerMethodField()
    units_list = serializers.SerializerMethodField()
    items_list = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'kts_list', 'units_list', 'items_list']

    def get_kts_list(self, obj):
        kts = ProjectKTS.objects.filter(project=obj)
        return ProjectKTSSerializer(kts, many=True).data

    def get_units_list(self, obj):
        units = ProjectUnit.objects.filter(project=obj)
        return ProjectUnitSerializer(units, many=True).data

    def get_items_list(self, obj):
        items = ProjectItem.objects.filter(project=obj)
        return ProjectItemSerializer(items, many=True).data
