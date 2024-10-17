from abc import ABC, abstractmethod
from typing import Iterable


class Model(ABC):

    def __init__(self, n_features: int, n_components: int):
        self.n_features = n_features
        self.n_components = n_components
        self.vectorizer = None
        self.model = None
        self.fitted = False

    @abstractmethod
    def fit(self, corpus: Iterable[str]) -> None:
        pass

    def get_feature_names(self) -> Iterable:
        if not self.fitted:
            raise ValueError("Model not fit, impossible to get feature names.")
        return self.vectorizer.get_feature_names_out()
