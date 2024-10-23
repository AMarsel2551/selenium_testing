from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


class WebDriverContextManager:
    def __init__(self):
        self.driver = None

    def __enter__(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")  # Запуск без интерфейса
        options.add_argument("--no-sandbox")  # Обход некоторых проблем с безопасностью
        options.add_argument("--disable-dev-shm-usage")  # Уменьшение использования памяти

        path = "/app/chromedriver"
        path = ChromeDriverManager().install()

        self.driver = webdriver.Chrome(path, chrome_options=options)
        return self.driver

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.driver:
            self.driver.quit()