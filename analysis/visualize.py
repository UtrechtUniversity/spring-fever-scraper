import math
from typing import Iterable

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
        items_by_topic: np.ndarray, dataset: pd.DataFrame, topic_id: int
):
    dominant_topic = np.argmax(items_by_topic,axis=1) + 1

    dataset['dominant_topic'] = dominant_topic

    return dataset[dataset['dominant_topic'] == topic_id][['original_text']]


