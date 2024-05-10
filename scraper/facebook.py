from typing import Generator, Optional

import facebook_scraper as fs
from tqdm import tqdm

from scraper.base import Scraper, Post
from scraper.utils import clean, get_author_id, replace_authors


class FacebookScraper(Scraper):

    def __init__(self, name: str, post_url: str, post_id: str,
                 cookies_path: Optional[str] = "cookies.json",
                 max_comments: Optional[int] = 100):
        """
        Functionality for scraping reactions from Facebook.
        Intended to be used for scraping reactions to a single
        post (including all reactions).

        Uses the implementation in `facebook_scraper`. Requires
        that a valid cookies.json is present, which can be
        generated using the get cookies.txt LOCALLY plugin
        on Chrome. See `facebook_scraper` docs for details.

        :param name: string identifier to be used in results
        :param post_url: the url for the post to be scraped
        :param post_id: the Facebook ID for the post
        :param cookies_path: path to a local cookies file
        :param max_comments: max number of comments to scrape
        """
        super().__init__(name)
        self.post_url = post_url
        self.post_id = post_id
        self.cookies_path = cookies_path
        self.max_comments = max_comments

    def fetch(self, post_id: str) -> Optional[fs.Post]:
        try:
            gen = fs.get_posts(
                post_urls=[post_id],
                options={"comments": self.max_comments, "progress": False, "allow_extra_requests": False},
                cookies=self.cookies_path,
                extra_info=True
            )
            post = next(gen)
            return post
        except Exception as e:
            print(f"An error occurred: {e}")
        return None

    def parse(self, post: fs.Post) -> Generator[tuple[int, str], None, None]:
        """
        Parse a single page of posts and responses. Yield the (anonymized) author and text.
        :param post: parsed DOM object containing the responses
        :return: as generator, tuples of author-ids and response texts
        """
        comments = post['comments_full']
        for comment in comments:
            yield (get_author_id(comment['commenter_name']),
                   replace_authors(clean(comment['comment_text']), no_space=True))
            for reply in comment['replies']:
                yield (get_author_id(reply['commenter_name']),
                       replace_authors(clean(reply['comment_text']), no_space=True))

    def run(self) -> Generator[Post, None, None]:
        if post := self.fetch(self.post_id):
            for author_id, text in tqdm(self.parse(post), f"Scraping {self.name}..."):
                post = Post(author_id, text, self.name, self.post_url)
                yield post

