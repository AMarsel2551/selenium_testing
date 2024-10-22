from scraper import Scraper

pretty_html = Scraper().scrape(link="https://api.ipify.org/").prettify()