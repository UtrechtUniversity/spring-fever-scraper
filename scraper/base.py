from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional, Generator

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm


@dataclass
class Post:
    author_id: int
    text: str
    name: str
    url: str


class Scraper(ABC):
    def __init__(self, name: str, base_url: str):
        """
        Base functionality to be used for any scraper. Assumes that a given page
        may have multiple sub-pages with an identical structure.
        :param name: string identifier to be used in results
        :param base_url: the page whose subpages should be scraped
        """
        self.name = name
        self.base_url = base_url
        self.subpages = None

    @staticmethod
    def fetch(url: str) -> Optional[BeautifulSoup]:
        """
        Fetch page HTML and parse with BeautifulSoup.
        :param url: url whose HTML must be fetched
        :return: parsed DOM as BeautifulSoup (if successful)
        """
        try:
            response = requests.get(url)
            response.raise_for_status()
            return BeautifulSoup(response.text, 'html.parser')
        except requests.RequestException as e:
            print(f"Request failed: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")
        return None

    @abstractmethod
    def collect_subpages(self):
        """
        Collect all subpages that are to be scraped and store in `self.subpages`.
        """
        pass

    @abstractmethod
    def parse(self, soup: BeautifulSoup) -> Generator[tuple[int, str], None, None]:
        """
        Parse a single page. Yield the (anonymized) author and text.
        :param soup: parsed DOM object containing the responses
        :return: as generator, tuples of author-ids and response texts
        """
        pass

    def run(self) -> Generator[Post, None, None]:
        """
        Iterate over subpages and retrieve required information.
        :return: relevant information as Post objects
        """
        self.collect_subpages()
        for url in tqdm(self.subpages, desc=f"Scraping {self.name}..."):
            if soup := self.fetch(url):
                for author_id, text in self.parse(soup):
                    yield Post(author_id, text, self.name, url)
