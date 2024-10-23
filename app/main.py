import time
import traceback

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


try:
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Запуск без интерфейса
    options.add_argument("--no-sandbox")  # Обход некоторых проблем с безопасностью
    options.add_argument("--disable-dev-shm-usage")  # Уменьшение использования памяти

    path = ChromeDriverManager().install()
    print(f"path 1: {path}")
    path = "./app/chromedriver/chromedriver-linux64/chromedriver"
    print(f"path 2: {path}")
    driver = webdriver.Chrome(path, options=options)


    driver.get('https://api.ipify.org')
    time.sleep(1)


    main_page = driver.page_source
    print(main_page)


    time.sleep(2)
    driver.quit()
except:
    print(f"traceback: {traceback.format_exc()}")


print("END")
time.sleep(5)


