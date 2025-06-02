#!/bin/bash

# Скрипт для автоматического создания суперпользователя admin/admin
# Работает даже если пользователь уже существует

echo "Создаём суперпользователя admin/admin, если он ещё не создан..."

# Команда в Django через manage.py shell
python manage.py shell << END
from django.contrib.auth import get_user_model

User = get_user_model()

if not User.objects.filter(username="admin").exists():
    User.objects.create_superuser("admin", "admin@example.com", "admin")
    print("✅ Суперпользователь admin/admin создан.")
else:
    print("ℹ️ Суперпользователь admin уже существует.")
END