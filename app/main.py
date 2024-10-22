import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

options = webdriver.ChromeOptions()
options.add_argument('--headless')

path = ChromeDriverManager().install()
print(f"path: {path}")
driver = webdriver.Chrome(path, options=options)


driver.get('https://api.ipify.org')
time.sleep(1)


main_page = driver.page_source
print(main_page)


time.sleep(2)
driver.quit()

