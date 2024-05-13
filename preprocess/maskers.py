import re

from preprocess import Preprocessor


class AccountMasker(Preprocessor):
    def __init__(self):
        self.regex = r'(@\d+$)'

    def __call__(self, sentence: str) -> str:
        return " ".join("USER" if re.match(self.regex, word) else word for word in sentence.split())