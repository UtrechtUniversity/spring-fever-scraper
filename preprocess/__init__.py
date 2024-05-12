from preprocess.base import Preprocessor
from preprocess.stemming import Stemmer

PREPROCESSORS = {
    'stemming': Stemmer
}


def load_preprocessor(kind: str, **kwargs) -> Preprocessor:
    if kind not in PREPROCESSORS:
        raise ValueError(f"Type {kind} not found. Available preprocessors: {PREPROCESSORS.keys()}")
    return PREPROCESSORS[kind](**kwargs)
