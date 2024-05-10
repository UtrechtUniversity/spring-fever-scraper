from typing import Generator


from scraper.base import Scraper, Post
from scraper.utils import get_author_id, replace_authors, clean


class YouTubeScraper(Scraper):

    def __init__(self, name: str):
        """
        TODO does not work yet
        Functionality for scraping video reactions from YouTube.
        Intended to be used for scraping reactions to a single
        video (including all reactions).
        :param name: string identifier to be used in results
        """
        super().__init__(name)

    def parse(self, video) -> Generator[tuple[int, str], None, None]:
        """
        Parse a single page of posts and responses. Yield the (anonymized) author and text.
        :param soup: parsed DOM object containing the responses
        :return: as generator, tuples of author-ids and response texts
        """
        pass

    def run(self) -> Generator[Post, None, None]:
        print(f"Scraping {self.name}...")
