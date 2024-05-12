from nltk.stem.snowball import DutchStemmer, PorterStemmer

from preprocess.base import Preprocessor

STEMMERS = {
    'porter': PorterStemmer,
    'snowball-dutch': DutchStemmer
}


class Stemmer(Preprocessor):
    def __init__(self, protocol: str):
        """
        Apply a stemming algorithm to the words in a sentence.
        :param protocol: stemming algorithm to be used.
        """
        super().__init__()
        if protocol not in STEMMERS:
            raise ValueError(f"Stemming protocol {protocol} not recognized.")
        self.stemmer = STEMMERS[protocol]()

    def __call__(self, sentence: str) -> str:
        """Apply the stemming algorithm."""
        return " ".join(self.stemmer.stem(word) for word in sentence.split())