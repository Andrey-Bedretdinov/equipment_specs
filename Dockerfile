# Dockerfile
FROM python:3.11-slim

# Чтобы pip не кешировал файлы и быстрее работало
ENV PYTHONUNBUFFERED=1

# Рабочая директория внутри контейнера
WORKDIR /app

# Копируем файл с зависимостями и сразу ставим их
COPY requirements.txt /app/
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Копируем всё содержимое проекта внутрь контейнера
COPY . /app/

# Делаем исполняемым файл entrypoint (опишем ниже)
RUN chmod +x /app/entrypoint.sh

# Открываем порт, на котором Django будет слушать
EXPOSE 8000

# По умолчанию запускаем наш скрипт-«точку входа»
ENTRYPOINT ["/app/entrypoint.sh"]