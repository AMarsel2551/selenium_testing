from fastapi import Body, FastAPI
from app.scraper import main as main_scraper


app = FastAPI(
    title="Scraping Ozon Api",
)


@app.post("/scraping/cards",)
async def scraping_cards(
    skus: list[str] = Body(..., description='skus')
):
    return await main_scraper(skus=skus)
