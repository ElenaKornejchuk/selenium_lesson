FROM python:3.11-slim

# Устанавливаем зависимости
RUN apt-get update && apt-get install -y \
    curl \
    unzip \
    chromium-driver \
    firefox-esr \
    && apt-get clean

# Устанавливаем pip-зависимости проекта
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект внутрь контейнера
COPY . .

# Команда по умолчанию — запуск pytest с возможностью передать параметры
ENTRYPOINT ["pytest"]