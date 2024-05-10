from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional, Generator, Any, Union

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm


@dataclass
class Post:
    author_id: Union[int, str]
    text: str
    name: str
    url: str


class Scraper(ABC):
    def __init__(self, name: str):
        """
        Base functionality to be used for any scraper.
        :param name: string identifier to be used in results
        """
        self.name = name

    @abstractmethod
    def parse(self, page: Any) -> Generator[tuple[Any, str], None, None]:
        """
        Parse a single page. Yield the (anonymized) author and text.
        :param page: page object containing the responses
        :return: as generator, tuples of author-ids and response texts
        """
        pass

    @abstractmethod
    def run(self) -> Generator[Post, None, None]:
        pass
