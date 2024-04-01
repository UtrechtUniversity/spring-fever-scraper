from scraper.base import Scraper


class OudersNLScraper(Scraper):

    def __init__(self, name: str, base_url: str):
        super().__init__(name, base_url)
        self.first_scraped = False

    def parse(self, soup):
        reactions = soup.find_all('div', class_='reaction-wrapper')

        # first post is included on every page, only scrape it once
        if self.first_scraped:
            reactions.pop(0)
        else:
            self.first_scraped = True

        for reaction in reactions:
            texts = reaction.find('div', class_='content').find_all('p', recursive=False)
            text = " ".join(t.text.strip() for t in texts).strip().replace("\n", " ")

            author_name = reaction.find('div', class_='author-information').find('h3').text.strip()
            aid = self.author_id(author_name)

            yield aid, text

    def collect_subpages(self):
        first_page = self.fetch(self.base_url)
        max_page = max(int(t.text)
                       for t in first_page.find_all("a", class_="page-link")
                       if all(i.isdigit() for i in t)) - 1
        self.subpages = [f"{self.base_url}?page={i}"
                         for i in range(max_page)]
