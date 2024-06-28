import string

import nltk
from bs4 import BeautifulSoup

nltk.download('stopwords')
from nltk.corpus import stopwords
import unicodedata

from preprocess import Preprocessor


class StopwordRemover(Preprocessor):
    def __init__(self):
        self.stop_words = set(stopwords.words('dutch'))

    def __call__(self, sentence: str) -> str:
        return " ".join(word for word in sentence.split() if word not in self.stop_words)


class PunctuationRemover(Preprocessor):
    @staticmethod
    def is_punctuation(char):
        return unicodedata.category(char).startswith('P') or char in set(string.punctuation)

    def __call__(self, sentence: str) -> str:
        no_punctuation = "".join(char for char in sentence if not self.is_punctuation(char))
        return " ".join(no_punctuation.split())


class HTMLTagRemover(Preprocessor):
    def __call__(self, sentence: str) -> str:
        soup = BeautifulSoup(sentence, "html.parser")
        return soup.get_text()
