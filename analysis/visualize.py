import math
from typing import Iterable

from matplotlib import pyplot as plt
from sklearn.base import BaseEstimator


def plot_top_words(
        model: BaseEstimator, n_components: int, feature_names: Iterable[str], n_top_words: int,
):
    fig, axes = plt.subplots(2, int(math.ceil(n_components/2)), figsize=(30, 15), sharex=True)
    axes = axes.flatten()
    for topic_idx, topic in enumerate(model.components_):
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
