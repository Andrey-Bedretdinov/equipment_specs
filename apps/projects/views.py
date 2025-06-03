from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Project
from .serializers import ProjectSerializer


@extend_schema_view(
    list=extend_schema(summary="Список проектов пользователя"),
    retrieve=extend_schema(summary="Детали проекта"),
    create=extend_schema(summary="Создать новый проект"),
    update=extend_schema(summary="Обновить проект"),
    partial_update=extend_schema(summary="Частичное обновление проекта"),
    destroy=extend_schema(summary="Удалить проект"),
)
class ProjectViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления проектами.

    Доступные операции:
    - получить список проектов
    - получить информацию о проекте
    - создать проект
    - изменить проект
    - удалить проект
    """

    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Project.objects.filter(created_by=self.request.user)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class ProjectFullTreeView(APIView):
    def get(self, request):
        projects = Project.objects.all()
        data = []

        for project in projects:
            kts_list = []
            for kts in project.projectkts_set.all():
                units_list = []
                for unit in kts.projectunit_set.all():
                    items_list = []
                    for item in unit.projectitem_set.all():
                        item_price = float(item.catalog_item.price) * item.quantity
                        items_list.append({
                            "id": item.id,
                            "name": item.catalog_item.name,
                            "description": item.catalog_item.description,
                            "supplier": item.catalog_item.supplier,
                            "catalog_code": item.catalog_item.catalog_code,
                            "price": float(item.catalog_item.price),
                            "currency": item.catalog_item.currency,
                            "manufactured": item.catalog_item.manufactured,
                            "delivery_type": item.catalog_item.delivery_type,
                            "quantity": item.quantity
                        })
                    unit_price_total = sum(i["price"] * i["quantity"] for i in items_list)
                    units_list.append({
                        "id": unit.id,
                        "name": unit.catalog_unit.name,
                        "description": unit.catalog_unit.description,
                        "price_total": unit_price_total,
                        "items": items_list
                    })
                kts_price_total = sum(u["price_total"] for u in units_list)
                kts_list.append({
                    "id": kts.id,
                    "name": kts.catalog_kts.name,
                    "description": kts.catalog_kts.description,
                    "price_total": kts_price_total,
                    "units": units_list
                })
            project_price_total = sum(k["price_total"] for k in kts_list)
            data.append({
                "id": project.id,
                "name": project.name,
                "description": project.description,
                "price_total": project_price_total,
                "kts": kts_list
            })

        return Response(data)
