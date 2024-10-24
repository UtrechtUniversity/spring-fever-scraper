import math
from typing import Iterable, List

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt


def plot_top_words(
        words_by_topic: np.ndarray, feature_names: Iterable[str], n_top_words: int,
):
    fig, axes = plt.subplots(2, int(math.ceil(words_by_topic.shape[0]/2)), figsize=(30, 15), sharex=True)
    axes = axes.flatten()
    for topic_idx, topic in enumerate(words_by_topic):
        top_features_ind = topic.argsort()[-n_top_words:]
        top_features = feature_names[top_features_ind]
        weights = topic[top_features_ind]

        ax = axes[topic_idx]
        ax.barh(top_features, weights, height=0.7)
        ax.set_title(f"Topic {topic_idx +1}", fontdict={"fontsize": 30})
        ax.tick_params(axis="both", which="major", labelsize=20)
        for i in "top right left".split():
            ax.spines[i].set_visible(False)

    plt.subplots_adjust(top=0.90, bottom=0.05, wspace=0.90, hspace=0.3)

    return fig


def plot_topic_distribution(
        items_by_topic: np.ndarray, dataset: pd.DataFrame, show_cols: List[str]
):

    topic_cols = [f"topic_{i+1}" for i in range(items_by_topic.shape[1])]

    dataset[topic_cols] = items_by_topic

    return dataset[[c for c in show_cols if c in dataset.columns] + topic_cols]


