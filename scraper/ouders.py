from scraper.base import Scraper
from scraper.utils import Reaction


class OudersNLScraper(Scraper):
    def parse(self, soup):
        reactions = soup.find_all('div', class_='reaction-wrapper')
        parsed = []
        for reaction in reactions[1:]:
            text = reaction.find('div', class_='content').find('p').text.strip()
            author_name = reaction.find('div', class_='author-information').find('h3').text.strip()
            aid = self.author_id(author_name)
            parsed.append(Reaction(
                aid, text, self.name
            ))

            print(f'{aid} - {text}')
        return parsed

    def collect_subpages(self):
        first_page = self.fetch(self.base_url)
        max_page = 12
        self.subpages = [
            f"{self.base_url}?page={i}"
            for i in range(max_page)
        ] # TODO write proper implementation

# TODO remove initial post
# TODO remove inline responses