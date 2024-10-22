FROM python:3.11-slim

# Установите необходимые пакеты
# Установите необходимые пакеты
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    gnupg \
    curl \
    libxss1 \
    libappindicator3-1 \
    libasound2 \
    libatk1.0-0 \
    libcups2 \
    libx11-xcb1 \
    libxcomposite1 \
    libxrandr2 \
    libxtst6 \
    libnss3 \
    libgtk-3-0 \
    chromium \
    chromium-driver \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*


WORKDIR /

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY ./app /app

WORKDIR /app

CMD python ./main.py
