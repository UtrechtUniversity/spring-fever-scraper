import csv
import os
from datetime import datetime

from confidence import load_name

from scraper import load_scraper


def main():
    """
    Main script for scraping websites defined in config/websites.yaml.
    Writes results to csv as they are retrieved.
    """

    config = load_name('config/websites')
    os.makedirs("scratch", exist_ok=True)
    filename = f"scratch/results_{datetime.now().strftime("%Y%m%d-%H%M%S")}.csv"

    with open(filename, "w", encoding='utf-8', newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["page_author_id", "text", "page_name", "url"])

        for website in config.websites:
            scraper = load_scraper(website.kind, **website.settings)
            for result in scraper.run():
                writer.writerow([result.author_id, result.text, result.name, result.url])


if __name__ == '__main__':
    main()
