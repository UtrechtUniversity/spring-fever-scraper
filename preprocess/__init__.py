from preprocess.base import Preprocessor
from preprocess.maskers import AccountMasker
from preprocess.removers import StopwordRemover, PunctuationRemover
from preprocess.normalizers import Stemmer, Lemmatizer

PREPROCESSORS = {
    'account-masker': AccountMasker,
    'lemmatizer': Lemmatizer,
    'punctuation-remover': PunctuationRemover,
    'stemmer': Stemmer,
    'stopword-remover': StopwordRemover
}


def load_preprocessor(kind: str, **kwargs) -> Preprocessor:
    if kind not in PREPROCESSORS:
        raise ValueError(f"Type {kind} not found. Available preprocessors: {PREPROCESSORS.keys()}")
    return PREPROCESSORS[kind](**kwargs)
