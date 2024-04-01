from dataclasses import dataclass


@dataclass
class Reaction:
    author_id: str
    text: str
    name: str
    url: str
