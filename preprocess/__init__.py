from typing import Callable

from preprocess.base import Preprocessor
from preprocess.maskers import AccountMasker
from preprocess.normalizers import Lemmatizer, Lowercaser, Stemmer
from preprocess.removers import HTMLTagRemover, PunctuationRemover, StopwordRemover
from preprocess.utils import read_from_csv, read_from_zip

PREPROCESSORS = {
    'account-masker': AccountMasker,
    'html-remover': HTMLTagRemover,
    'lemmatizer': Lemmatizer,
    'lowercaser': Lowercaser,
    'punctuation-remover': PunctuationRemover,
    'stemmer': Stemmer,
    'stopword-remover': StopwordRemover
}

FILE_READERS = {
    'csv': read_from_csv,
    'zip': read_from_zip
}


def load_preprocessor(kind: str, **kwargs) -> Preprocessor:
    if kind not in PREPROCESSORS:
        raise ValueError(f"Type {kind} not found. Available preprocessors: {PREPROCESSORS.keys()}")
    return PREPROCESSORS[kind](**kwargs)


def load_filereader(kind: str) -> Callable:
    if kind not in FILE_READERS:
        raise ValueError(f"Type {kind} not found. Available file readers: {FILE_READERS.keys()}")
    return FILE_READERS[kind]
