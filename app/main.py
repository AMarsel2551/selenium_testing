import traceback
from app.seleniumes import WebDriverContextManager
from fastapi import Body, FastAPI, Path
from app.scraper import main as main_scraper


app = FastAPI(
    title="Scraping Ozon Api",
)


@app.post("/scraping/cards",)
async def scraping_cards(
    skus: list[str] = Body(..., description='skus')
):
    return await main_scraper(skus=skus)
