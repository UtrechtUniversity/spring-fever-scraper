from scraper.ouders import OudersNLScraper


def main():

    scrapers = [
        OudersNLScraper(
            name="Ouders.nl - alles over sex bespreken",
            base_url='https://www.ouders.nl/forum/ouders-en-school/alles-over-sex-bespreken-op-de-lagere-school'
        )
    ]

    for scraper in scrapers:
        scraper.run()


if __name__ == '__main__':
    main()
