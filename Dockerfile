# Используем официальный образ Python
FROM python:3.11-slim

# Устанавливаем рабочую директорию в /app
WORKDIR /

# Копируем файлы зависимостей и устанавливаем их
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY ./app /app

WORKDIR /app

CMD python ./main.py
