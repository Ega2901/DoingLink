#Используем базовый образ Python
FROM python:3.10

# Устанавливаем Redis
RUN apt-get update && \
    apt-get install -y redis-server && \
    rm -rf /var/lib/apt/lists/*

# Устанавливаем рабочую директорию
WORKDIR /app

ENV TZ=Europe/Moscow
# Копируем файлы зависимостей
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN pip install -U pip aiogram pytz && apt-get update && apt-get install sqlite3
# Копируем остальные файлы проекта в рабочую директорию
COPY . .

CMD ["python", "main.py"]
