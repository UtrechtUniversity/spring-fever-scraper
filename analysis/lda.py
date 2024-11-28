from abc import ABC
from typing import Iterable

from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer

from analysis import Model


class LDAModel(Model, ABC):

    def fit(self, corpus: Iterable[str]):
        self.vectorizer = CountVectorizer(
            max_df=0.95, min_df=2, max_features=self.n_features
        )
        tf_features = self.vectorizer.fit_transform(corpus)

        self.model = LatentDirichletAllocation(
            n_components=self.n_components,
            max_iter=5,
            learning_method="online",
            learning_offset=50.0,
            random_state=0,
        )
        self.items_by_topic = self.model.fit_transform(tf_features)
        self.items_by_topic_normalized = self.items_by_topic / self.items_by_topic.sum(axis=1, keepdims=True)
        self.fitted = True
