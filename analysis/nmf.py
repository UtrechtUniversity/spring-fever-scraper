from abc import ABC
from typing import Iterable

from sklearn.decomposition import NMF
from sklearn.feature_extraction.text import TfidfVectorizer

from analysis import Model


class NMFModel(Model, ABC):

    def fit(self, corpus: Iterable[str]):
        self.vectorizer = TfidfVectorizer(
            max_df=0.95, min_df=2, max_features=self.n_features
        )
        tfidf_features = self.vectorizer.fit_transform(corpus)
        self.items_by_topic = self.model.fit_transform(tfidf_features)
        self.fitted = True


class NMFFrobeniusModel(NMFModel):

    def __init__(self, n_features: int, n_components: int):
        super().__init__(n_features, n_components)
        self.model = NMF(
            n_components=n_components,
            random_state=1,
            init="nndsvda",
            beta_loss="frobenius",
            alpha_W=0.00005,
            alpha_H=0.00005,
            l1_ratio=1,
        )


class NMFKullbackLeiblerModel(NMFModel):

    def __init__(self, n_features: int, n_components: int):
        super().__init__(n_features, n_components)
        self.model = NMF(
            n_components=n_components,
            random_state=1,
            init="nndsvda",
            beta_loss="kullback-leibler",
            solver="mu",
            max_iter=1000,
            alpha_W=0.00005,
            alpha_H=0.00005,
            l1_ratio=0.5,
        )