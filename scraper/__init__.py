from scraper.base import Scraper
from scraper.facebook import FacebookScraper
from scraper.ouders import OudersNLScraper
from scraper.youtube import YouTubeScraper

SCRAPERS = {
    "facebook": FacebookScraper,
    'ouders.nl': OudersNLScraper,
    "youtube": YouTubeScraper
}


def load_scraper(kind: str, **kwargs) -> Scraper:
    if kind not in SCRAPERS:
        raise ValueError(f"Type {kind} not found. Available scrapers: {SCRAPERS.keys()}")
    return SCRAPERS[kind](**kwargs)
