import csv
import os

from confidence import load_name

from scraper.utils import load_scraper


def main():
    config = load_name('config/websites')

    all_results = []
    for website in config.websites:
        scraper = load_scraper(website.kind, **website.settings)
        all_results += scraper.run()

    os.makedirs("scratch", exist_ok=True)
    with open("scratch/results.csv", "w", encoding='utf-8', newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["page_author_id", "text", "page_name", "url"])
        for result in all_results:
            writer.writerow([result.author_id, result.text, result.name, result.url])


if __name__ == '__main__':
    main()
