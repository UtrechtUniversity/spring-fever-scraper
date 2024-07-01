from typing import Generator, Optional

from confidence import load_name
from googleapiclient.discovery import build
from tqdm import tqdm

from scraper.base import Post, Scraper
from scraper.utils import AuthorHandler


class YouTubeScraper(Scraper):

    def __init__(self, name: str, video_id: str, author_handler: AuthorHandler,
                 api_yaml: Optional[str] = "credentials/yt_apikey"):
        """
        Functionality for scraping video reactions from YouTube.
        Intended to be used for scraping reactions to a single
        video (including all reactions).

        Requires an API key to access the YouTube Data API V3.

        :param name: string identifier to be used in results
        :param video_id: id of video (end of youtube URL)
        :param author_handler: class for replacing authors by id
        :param api_yaml: location of the yaml file with the API key
        """
        super().__init__(name)
        self.video_id = video_id
        self.video_url = f"https://www.youtube.com/watch?v={self.video_id}"
        self.api_key = load_name(api_yaml).api_key
        self.author_handler = author_handler

    def fetch_comment_pages(self, video_id: str) -> Optional[list[dict]]:
        """
        Comments are returned in multiple pages/batches. Keep requesting new
        comments until the API returns no more.
        :param video_id: identifier of the video on YouTube
        :return: a list of the pages/batches with comments resulting from API calls
        """
        pages = []
        try:
            youtube = build('youtube', 'v3', developerKey=self.api_key)
            request = youtube.commentThreads().list(
                part="snippet,replies",
                videoId=video_id,
                textFormat="plainText"
            )
            while request:
                response = request.execute()
                pages.append(response)
                request = youtube.commentThreads().list_next(request, response)
            return pages
        except Exception as e:
            print(f"An error occurred: {e}")
        return None

    def parse(self, video: dict) -> Generator[tuple[int, str], None, None]:
        """
        Parse a single page/batch of comments. Yield the author-id and text.
        :param video: API response object containing the comments
        :return: as generator, tuples of author-ids and response texts
        """
        for item in video['items']:
            comment = item['snippet']['topLevelComment']['snippet']
            yield self.author_handler.get_author_id(comment['authorDisplayName']), comment['textDisplay']

            if item['snippet']['totalReplyCount'] > 0:
                for reply in item['replies']['comments']:
                    reply_message = reply['snippet']
                    yield (self.author_handler.get_author_id(reply_message['authorDisplayName']),
                           reply_message['textDisplay'])

    def run(self) -> Generator[Post, None, None]:
        if pages := self.fetch_comment_pages(self.video_id):
            for page in tqdm(pages, f"Scraping {self.name}..."):
                for author_id, text in self.parse(page):
                    post = Post(author_id, text, self.name, self.video_url)
                    yield post
