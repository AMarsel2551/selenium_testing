from selenium.common.exceptions import TimeoutException
from app.logger import log
from app.models import Product, Price
from app.seleniumes import WebDriverContextManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from typing import Any


TIMEOUT_ELEMENT = 2.5


def drive_error(func):
    def wrapper(*args, **kwargs):
        try:
            r =  func(*args, **kwargs)
            # log.info(f"func_name: {func.__name__} is ok")
            return r

        except TimeoutException:
            log.warning(f"func_name: {func.__name__} error: timeout")
        except Exception as error:
            log.warning(f"func_name: {func.__name__} error: {error}")
        return None
    return wrapper


@drive_error
def click(wait):
    try:
        reload_button = wait.until(EC.element_to_be_clickable((By.ID, "reload-button")))
        reload_button.click()
    except:
        pass


@drive_error
def get_final_price(wait) -> int:
    element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "span.s5m_27.ms4_27")))
    price = int(element.text.replace(" ", "").replace("₽", ""))
    return price


def get_basic_price(wait) -> int | None:
    try:
        element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "span.mt_27.tm0_27.ms9_27.tm_277")))
        price = int(element.text.replace(" ", "").replace("₽", ""))
        return price
    except:
        return None


def get_price(wait) -> dict:
    final_price = get_final_price(wait=wait)
    price = get_basic_price(wait=wait)
    if price is None:
        price = final_price

    if final_price and price:
        discount = round(100 - (final_price / (price/100)))
    else:
        discount = None
    return {
        "price": price,
        "discount": discount,
        "final_price": final_price,
    }


@drive_error
def get_name(wait) -> str:
    element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "h1.tm6_27.tsHeadline550Medium")))
    return element.text


@drive_error
def get_seller(wait) -> str:
    element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "kv2_27")))
    return element.get_attribute("title")


@drive_error
def get_brand_and_category(wait) -> dict:
    ol_element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'je1_10')))
    elements = ol_element.find_elements(By.TAG_NAME, 'li')
    elements_text = [element.text for element in elements]
    return {"brand": elements_text[-1], "category": elements_text[-2]}


@drive_error
def get_photo(wait) -> Any:
    images = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.t8l_27 img")))
    image_urls = [img.get_attribute('src') for img in images]
    for image_url in image_urls:
        if "video" in image_url:
            continue
        if "wc" not in image_url:
            continue
        return image_url.replace("wc50", "wc1000")
    return None


@drive_error
def get_rating(wait) -> float:
    element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "ga115-a2.tsBodyControl500Medium")))
    rating = float(element.text.split(' • ')[0])
    return rating


def start(driver, data: list, sku: str, i: int) -> list:
    try:
        driver.get(f"https://www.ozon.ru/product/{sku}/?oos_search=false")
        wait = WebDriverWait(driver=driver, timeout=TIMEOUT_ELEMENT)

        if i == 0:
            click(wait=wait)

        # Извлечение цены 1170 ₽
        price = get_price(wait=wait)

        # Извлечение названия товара
        name = get_name(wait=wait)

        # seller
        seller = get_seller(wait=wait)

        # brand and category
        brand_category = get_brand_and_category(wait=wait)
        if isinstance(brand_category, dict):
            brand = brand_category['brand']
            category = brand_category['category']
        else:
            brand = None
            category = None

        # photo
        photo = get_photo(wait=wait)

        # rating
        rating = get_rating(wait=wait)

        obj = {
            "sku": sku,
            "category": category,
            "name": name,
            "seller": seller,
            "brand": brand,
            "photo": photo,
            "rating": rating,
            "price": price,
        }
        data.append(Product(**obj))
    except Exception as error:
        log.error(f"error: {error}")
    return data


async def main(skus: list=None) -> list:
    data = []
    with WebDriverContextManager() as driver:
        for i, sku in enumerate(skus):
            data = start(driver=driver, data=data, sku=sku, i=i)

    data = [d.dict() for d in data]
    return data
