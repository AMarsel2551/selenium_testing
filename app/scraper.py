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
            return func(*args, **kwargs)

        except TimeoutException:
            print(f"func_name: {func.__name__} error: timeout")
        except Exception as error:
            print(f"func_name: {func.__name__} error: {error}")
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
    element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".m2s_27.sm0_27")))
    price = int(element.text.replace(" ", "").replace("₽", ""))
    return price


def get_basic_price(wait) -> int | None:
    try:
        element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "span.sm6_27.sm7_27.sm5_27.s6m_27")))
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
    element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "h1.mt3_27.tsHeadline550Medium")))
    return element.text


@drive_error
def get_seller(wait) -> str:
    element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "k9u_27")))
    return element.get_attribute("title")


@drive_error
def get_brand_and_category(wait) -> tuple[str, str]:
    elements = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//a[contains(@class, "a6 j0e_10")]/span')))
    elements_text = [element.text for element in elements]
    brand = elements_text[-1]
    category = elements_text[-2]
    return brand, category


@drive_error
def get_photo(wait) -> Any:
    images = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.u5k_27 img")))
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
        driver.get(f"https://www.ozon.ru/product/{sku}")
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
        brand, category = get_brand_and_category(wait=wait)

        # photo
        photo = get_photo(wait=wait)

        # rating
        rating = get_rating(wait=wait)

        data.append(Product(
            sku=sku,
            category=category,
            name=name,
            seller=seller,
            brand=brand,
            photo=photo,
            rating=rating,
            price=Price(**price),
        ))
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
