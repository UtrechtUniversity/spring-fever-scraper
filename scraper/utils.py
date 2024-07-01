from typing import Dict, Optional, Sequence

import yaml


class AuthorHandler:
    def __init__(self, authors: Optional[Sequence] = None):
        self.authors = authors or []

    def get_author_id(self, author: str) -> int:
        """Replace author account name by id"""
        if author not in self.authors:
            self.authors.append(author)
        return self.authors.index(author)

    def replace_authors(self, text: str) -> str:
        """Replace name of authors/accounts in text"""
        for author in self.authors:
            text = text.replace(f"@{author}", f"@{self.get_author_id(author)}")
            text = text.replace(f"{author} ", f"@{self.get_author_id(author)} ")
            text = text.replace(author, f"@{self.get_author_id(author)}")
        return text


def clean(text: str) -> str:
    """Simple cleaning of strings"""
    return " ".join(text.split())


def read_yaml_utf8(path: str) -> Dict:
    """Read a yaml file using utf-8 encoding"""
    with open(path, 'r', encoding='utf-8') as file:
        data = yaml.safe_load(file)
    return data
