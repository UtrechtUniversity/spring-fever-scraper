import csv
import os
from datetime import datetime

from confidence import Configuration, load_name

from scraper import load_scraper
from scraper.utils import AuthorHandler, clean, read_yaml_utf8


def main():
    """
    Main script for scraping websites defined in config/scrape.yaml.
    Writes results to csv as they are retrieved.
    """

    config = load_name('config/scrape')
    os.makedirs("scratch", exist_ok=True)
    filename = f"scratch/results_{datetime.now().strftime('%Y%m%d-%H%M%S')}.csv"

    author_handler = AuthorHandler(authors=list(read_yaml_utf8('config/local.yaml')['authors']))
    global_settings = {'author_handler': author_handler}

    with open(filename, "w", encoding='utf-8', newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["page_author_id", "text", "page_name", "url"])

        for website in config.websites:
            scraper = load_scraper(website.kind, **Configuration(global_settings, website.settings))
            website_posts = [post for post in scraper.run()]
            for post in website_posts:
                writer.writerow(
                    [post.author_id, author_handler.replace_authors(clean(post.text)), post.name, post.url]
                )


if __name__ == '__main__':
    main()
