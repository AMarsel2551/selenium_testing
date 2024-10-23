import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


class WebDriverContextManager:
    def __init__(self):
        self.driver = None

    def __enter__(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")  # Запуск без интерфейса
        options.add_argument("--no-sandbox")  # Обход некоторых проблем с безопасностью
        options.add_argument("--disable-dev-shm-usage")  # Уменьшение использования памяти
        self.driver = webdriver.Chrome("/app/chromedriver", chrome_options=options)
        return self.driver

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.driver:
            self.driver.quit()