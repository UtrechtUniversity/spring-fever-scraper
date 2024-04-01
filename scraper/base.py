from abc import ABC
from dataclasses import dataclass
from typing import Optional

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm


@dataclass
class Post:
    author_id: str
    text: str
    name: str
    url: str


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

    def run(self) -> list[Post]:
        self.collect_subpages()
        results = []
        for url in tqdm(self.subpages[:2], desc=f"Scraping pages of {self.name}..."):
            if soup := self.fetch(url):
                for author_id, text in self.parse(soup):
                    results.append(
                        Post(author_id, text, self.name, url)
                    )
        return results

    def author_id(self, author: str) -> int:
        """Replace author account name by id"""
        if author not in self.authors:
            self.authors.append(author)
        return self.authors.index(author)

    def replace_authors(self, text: str) -> str:
        """Replace name of authors/accounts in text"""
        for author in self.authors:
            text = text.replace(f" {author} ", f" {self.author_id(author)}")
            text = text.replace(f"@{author} ", f"@{self.author_id(author)}")
        return text
