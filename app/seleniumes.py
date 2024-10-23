from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


# PATH = "/app/chromedriver"
PATH = ChromeDriverManager().install()


class WebDriverContextManager:
    def __init__(self):
        self.driver = None

    def __enter__(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        self.driver = webdriver.Chrome(PATH, chrome_options=options)
        return self.driver

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.driver:
            self.driver.quit()