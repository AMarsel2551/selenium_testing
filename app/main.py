import time
import traceback
from selenium import webdriver


try:
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Запуск без интерфейса
    options.add_argument("--no-sandbox")  # Обход некоторых проблем с безопасностью
    options.add_argument("--disable-dev-shm-usage")  # Уменьшение использования памяти
    driver = webdriver.Chrome("/app/chromedriver", options=options)


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


