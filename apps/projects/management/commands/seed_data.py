from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from apps.items.models import Item
from apps.kts.models import KTS
from apps.projects.models import Project
from apps.units.models import Unit

User = get_user_model()


class Command(BaseCommand):
    help = "Seed database with test data"

    def handle(self, *args, **kwargs):
        # Удаляем старые тестовые данные (если были)
        Item.objects.all().delete()
        Unit.objects.all().delete()
        KTS.objects.all().delete()
        Project.objects.all().delete()
        User.objects.exclude(is_superuser=True).delete()

        # Создание пользователя
        user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='password123'
        )

        # Создание проекта
        project = Project.objects.create(
            name="Диспетчерская система",
            description="Спецификация оборудования для ЦОД",
            created_by=user
        )

        # КТС и комплектные единицы
        kts_server = KTS.objects.create(project=project, name="Серверная")
        kts_workplace = KTS.objects.create(project=project, name="Рабочее место диспетчера")

        unit_server_a = Unit.objects.create(kts=kts_server, name="Сервер А")
        unit_rack = Unit.objects.create(kts=kts_server, name="Шкаф напольный")
        unit_arm_1 = Unit.objects.create(kts=kts_workplace, name="АРМ Диспетчер 1")

        # Изделия
        Item.objects.create(
            unit=unit_server_a,
            name="Сервер Dell R740",
            supplier="Dell",
            catalog_code="R740-12345",
            quantity=1,
            price=4000.00,
            manufacturer="Dell",
            currency="USD",
            delivery_type="DDP"
        )

        Item.objects.create(
            unit=unit_server_a,
            name="SSD 2TB",
            supplier="Samsung",
            catalog_code="SSD-2TB-5678",
            quantity=2,
            price=300.00,
            manufacturer="Samsung",
            currency="USD",
            delivery_type="EXW"
        )

        Item.objects.create(
            unit=unit_rack,
            name="Кабель питания 5м",
            supplier="Legrand",
            catalog_code="CAB-5M-999",
            quantity=3,
            price=50.00,
            manufacturer="Legrand",
            currency="USD",
            delivery_type="FOB"
        )

        Item.objects.create(
            unit=unit_arm_1,
            name="Монитор Samsung 24\"",
            supplier="Samsung",
            catalog_code="MON-24-SAM",
            quantity=1,
            price=200.00,
            manufacturer="Samsung",
            currency="USD",
            delivery_type="DDP"
        )

        Item.objects.create(
            unit=unit_arm_1,
            name="Клавиатура Logitech",
            supplier="Logitech",
            catalog_code="KEY-LOGI-001",
            quantity=1,
            price=50.00,
            manufacturer="Logitech",
            currency="USD",
            delivery_type="CIF"
        )

        Item.objects.create(
            unit=unit_arm_1,
            name="Системный блок",
            supplier="HP",
            catalog_code="SYS-HP-5000",
            quantity=1,
            price=800.00,
            manufacturer="HP",
            currency="USD",
            delivery_type="DDP"
        )

        self.stdout.write(self.style.SUCCESS('Successfully seeded the database!'))
