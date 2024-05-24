import nltk
nltk.download('wordnet')

from nltk.stem.snowball import DutchStemmer
import spacy

from preprocess.base import Preprocessor


class Stemmer(Preprocessor):
    def __init__(self):
        """
        Apply a stemming algorithm to the words in a sentence.
        """
        self.stemmer = DutchStemmer()

    def __call__(self, sentence: str) -> str:
        return " ".join(self.stemmer.stem(word) for word in sentence.split())


class Lemmatizer(Preprocessor):

    def __init__(self):
        self.nlp = spacy.load("nl_core_news_lg")

    def __call__(self, sentence: str) -> str:
        doc = self.nlp(sentence)
        return " ".join(token.lemma_ for token in doc)
