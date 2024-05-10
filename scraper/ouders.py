from typing import Generator

from bs4 import BeautifulSoup

from scraper.web import WebScraper
from scraper.utils import get_author_id, replace_authors, clean


class OudersNLScraper(WebScraper):

    def __init__(self, name: str, base_url: str):
        """
        Functionality for scraping forum posts and responses from www.ouders.nl.
        Intended to be used for scraping a single forum post (including all pages).
        :param name: string identifier to be used in results
        :param base_url: the url for the forum post to be scraped
        """
        super().__init__(name, base_url)
        self.first_scraped = False

    def parse(self, soup: BeautifulSoup) -> Generator[tuple[int, str], None, None]:
        """
        Parse a single page of posts and responses. Yield the (anonymized) author and text.
        :param soup: parsed DOM object containing the responses
        :return: as generator, tuples of author-ids and response texts
        """
        reactions = soup.find_all('div', class_='reaction-wrapper')

        # first post is included on every page, only scrape it once
        if self.first_scraped:
            reactions.pop(0)
        else:
            self.first_scraped = True

        for reaction in reactions:
            author_name = reaction.find('div', class_='author-information').find('h3').text.strip()
            aid = get_author_id(author_name)

            texts = reaction.find('div', class_='content').find_all('p', recursive=False)
            text = clean(" ".join(t.text.strip() for t in texts))
            text = replace_authors(text)

            yield aid, text

    def collect_subpages(self) -> None:
        """
        Collect all subpages on which reactions can be found (if there are more than 15 responses,
        these are split into multiple pages).
        """
        first_page = self.fetch(self.base_url)
        max_page = max(int(t.text)
                       for t in first_page.find_all("a", class_="page-link")
                       if all(i.isdigit() for i in t))
        self.subpages = [f"{self.base_url}?page={i}"
                         for i in range(max_page)]
