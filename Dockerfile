# Базовый образ Python
FROM python:3.12-slim

# Настройки Python: запрет создания файлов .pyc и мгновенный вывод логов
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app/backend

# Устанавливаем рабочую директорию
WORKDIR /app

# Устанавливаем системные зависимости (curl для healthcheck и отладки)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Копируем файл зависимостей и устанавливаем их
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем исходный код проекта
COPY . .

# Делаем entrypoint скрипт исполняемым
RUN chmod +x /app/entrypoint.sh

# Открываем порт FastAPI приложения
EXPOSE 8000

# Запускаем миграции и затем приложение
ENTRYPOINT ["/app/entrypoint.sh"]
