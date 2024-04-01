from scraper.base import Scraper
from scraper.ouders import OudersNLScraper

SCRAPERS = {
    'ouders.nl': OudersNLScraper
}


def load_scraper(kind: str, **kwargs) -> Scraper:
    if kind not in SCRAPERS:
        raise ValueError(f"Type {kind} not found. Available scrapers: {SCRAPERS.keys()}")
    return SCRAPERS[kind](**kwargs)
