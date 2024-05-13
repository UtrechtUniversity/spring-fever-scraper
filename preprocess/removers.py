import string

import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords

from preprocess import Preprocessor


class StopwordRemover(Preprocessor):
    def __init__(self):
        self.stop_words = set(stopwords.words('dutch'))

    def __call__(self, sentence: str) -> str:
        return " ".join(word for word in sentence.split() if word not in self.stop_words)


class PunctuationRemover(Preprocessor):
    def __init__(self):
        self.punctuation_chars = set(string.punctuation)

    def __call__(self, sentence: str) -> str:
        return "".join(char for char in sentence if char not in self.punctuation_chars)
