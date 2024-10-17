from abc import ABC, abstractmethod
from typing import Iterable

import numpy as np


class Model(ABC):

    def __init__(self, n_features: int, n_components: int):
        self.n_features = n_features
        self.n_components = n_components
        self.vectorizer = None
        self.model = None
        self._words_by_topic = None
        self.items_by_topic = None
        self._feature_names = None
        self.fitted = False

    @abstractmethod
    def fit(self, corpus: Iterable[str]) -> None:
        pass

    @property
    def feature_names(self) -> Iterable[str]:
        if not self.fitted:
            raise ValueError("Model not fit, impossible to get feature names.")
        if self._feature_names is None:
            self._feature_names = self.vectorizer.get_feature_names_out()
        return self._feature_names

    @property
    def words_by_topic(self) -> np.ndarray:
        if not self.fitted:
            raise ValueError("Model not fit, impossible to get words by topic.")
        if not self._words_by_topic:
            self._words_by_topic = self.model.components_
        return self._words_by_topic
