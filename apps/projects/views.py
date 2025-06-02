from io import BytesIO

import openpyxl
from django.http import HttpResponse
from drf_spectacular.utils import extend_schema_view, extend_schema
from openpyxl.styles import Font
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import BaseRenderer
from rest_framework.response import Response

from .models import Project
from .serializers import ProjectSerializer


@extend_schema_view(
    list=extend_schema(description="Получить список всех проектов."),
    retrieve=extend_schema(description="Получить детали проекта."),
    create=extend_schema(description="Создать новый проект."),
    update=extend_schema(description="Обновить проект."),
    destroy=extend_schema(description="Удалить проект."),
)
class ProjectViewSet(viewsets.ModelViewSet):
    """
        Управление проектами: создание, получение списка, обновление и удаление.
    """
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=['get'], url_path='view')
    def view_specification(self, request, pk=None):
        project = self.get_object()
        data = []

        for kts in project.kts.all():
            kts_data = {
                'id': kts.id,
                'name': kts.name,
                'units': []
            }
            for unit in kts.units.all():
                unit_data = {
                    'id': unit.id,
                    'name': unit.name,
                    'items': []
                }
                for item in unit.items.all():
                    item_data = {
                        'id': item.id,
                        'name': item.name,
                        'supplier': item.supplier,
                        'catalog_code': item.catalog_code,
                        'quantity': item.quantity,
                        'price': float(item.price),
                        'manufacturer': item.manufacturer,
                        'currency': item.currency,
                        'delivery_type': item.delivery_type
                    }
                    unit_data['items'].append(item_data)
                kts_data['units'].append(unit_data)
            data.append(kts_data)

        return Response({'project': project.name, 'kts': data})

    class BinaryRenderer(BaseRenderer):
        media_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        format = 'xlsx'
        charset = None

        def render(self, data, media_type=None, renderer_context=None):
            return data

    @action(detail=True, methods=['get'], url_path='report', renderer_classes=[BinaryRenderer])
    def generate_report(self, request, pk=None):
        project = self.get_object()

        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Закупочная ведомость"

        # заголовки
        headers = [
            'Комплекс', 'Комплектная единица', 'Изделие', 'Поставщик',
            'Артикул', 'Количество', 'Цена', 'Производитель', 'Валюта', 'Тип поставки'
        ]
        ws.append(headers)

        bold_font = Font(bold=True)
        for col in range(1, len(headers) + 1):
            ws.cell(row=1, column=col).font = bold_font

        # данные
        for kts in project.kts.all():
            for unit in kts.units.all():
                for item in unit.items.all():
                    ws.append([
                        kts.name,
                        unit.name,
                        item.name,
                        item.supplier,
                        item.catalog_code,
                        item.quantity,
                        float(item.price),
                        item.manufacturer,
                        item.currency,
                        item.delivery_type
                    ])

        output = BytesIO()
        wb.save(output)
        output.seek(0)

        response = HttpResponse(
            output.read(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        filename = f"{project.name.replace(' ', '_')}_report.xlsx"
        response['Content-Disposition'] = f'attachment; filename={filename}'

        return response
