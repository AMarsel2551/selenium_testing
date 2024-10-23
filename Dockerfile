FROM python:3.11-slim

# Установите необходимые пакеты
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
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
    && wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update && apt-get install -y google-chrome-stable \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*


WORKDIR /

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY ./app /app

WORKDIR /app

#CMD python ./main.py
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port 8080 --workers 1 --log-level info"]
