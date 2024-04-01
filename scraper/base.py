from abc import ABC
from typing import Optional

import requests
from bs4 import BeautifulSoup


class Scraper(ABC):
    def __init__(self, name: str, base_url: str):
        self.name = name
        self.base_url = base_url
        self.subpages = None
        self.authors = []

    def fetch(self, url) -> Optional[BeautifulSoup]:
        try:
            response = requests.get(url)
            response.raise_for_status()
            return BeautifulSoup(response.text, 'html.parser')
        except requests.RequestException as e:
            print(f"Request failed: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")
        return None

    def collect_subpages(self) -> list[str]:
        raise NotImplementedError("Subclasses must implement collect_subpages method")

    def parse(self, soup):
        raise NotImplementedError("Subclasses must implement parse method")

    def run(self):
        results = []
        self.collect_subpages()
        for url in self.subpages:
            if soup := self.fetch(url):
                results += self.parse(soup)
        return results

    def author_id(self, author: str) -> int:
        """Replace author name by id"""
        if author not in self.authors:
            self.authors.append(author)
        return self.authors.index(author)
