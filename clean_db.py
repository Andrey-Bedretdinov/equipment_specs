# В PyCharm File -> New Python File -> clean_db.py (например)
import os

import django

from equipment_specs import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'equipment_specs.settings')
django.setup()

from apps.projects.models import Project

# в скрипте:
settings.DATABASES['default']['HOST'] = '192.168.31.200'

def clear_database():
    print("Удаляю все проекты каскадом...")
    Project.objects.all().delete()
    print("Готово!")


if __name__ == "__main__":
    clear_database()
