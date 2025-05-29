# Вихідний образ
FROM python:3.11-slim

# Встановлюємо робочу директорію
WORKDIR /app

# Копіюємо залежності
COPY requirements.txt .

# Встановлюємо залежності
RUN pip install --no-cache-dir -r requirements.txt

# Копіюємо весь код проєкту в контейнер
COPY . .

# Відкриваємо порт
EXPOSE 8000

# Запускаємо сервер (manage.py знаходиться в корені проєкту)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
