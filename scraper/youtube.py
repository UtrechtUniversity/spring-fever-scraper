from typing import Generator

from bs4 import BeautifulSoup

from scraper.base import Scraper
from scraper.utils import get_author_id, replace_authors


class YouTubeScraper(Scraper):

    def __init__(self, name: str, base_url: str):
        """
        TODO does not work yet
        Functionality for scraping video reactions from YouTube.
        Intended to be used for scraping reactions to a single
        video (including all reactions).
        :param name: string identifier to be used in results
        :param base_url: the url for the forum post to be scraped
        """
        super().__init__(name, base_url)

    def parse(self, soup: BeautifulSoup) -> Generator[tuple[int, str], None, None]:
        """
        Parse a single page of posts and responses. Yield the (anonymized) author and text.
        :param soup: parsed DOM object containing the responses
        :return: as generator, tuples of author-ids and response texts
        """
        reactions = soup.find_all('div', class_='reaction-wrapper')
        pass

    def collect_subpages(self) -> None:
        """
        On YouTube, the only page is the initial page (no real subpages exist).
        """

        self.subpages = [self.base_url]
