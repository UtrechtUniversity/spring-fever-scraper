import math
from typing import Iterable, List, Optional

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.ticker import MaxNLocator


def plot_top_words(
        words_by_topic: np.ndarray, feature_names: Iterable[str], n_top_words: int,
) -> plt.Figure:
    """
    Make bar plot with words by topic.
    :param words_by_topic: outcome of topic model
    :param feature_names: the words
    :param n_top_words: the number of words to display in plot
    :return: the bar plots for all topics
    """
    fig, axes = plt.subplots(2, int(math.ceil(words_by_topic.shape[0] / 2)), figsize=(25, 10), sharex=True)
    axes = axes.flatten()
    for topic_idx, topic in enumerate(words_by_topic):
        top_features_ind = topic.argsort()[-n_top_words:]
        top_features = feature_names[top_features_ind]
        weights = topic[top_features_ind]

        ax = axes[topic_idx]
        ax.barh(top_features, weights, height=0.8)
        ax.set_title(f"Topic {topic_idx + 1}", fontdict={"fontsize": 15})
        ax.tick_params(axis="both", which="major", labelsize=12)

        for i in ["top", "bottom", "right", "left"]:
            ax.spines[i].set_visible(False)
        ax.xaxis.set_visible(False)

    for idx in range(len(words_by_topic), len(axes)):
        fig.delaxes(axes[idx])

    plt.subplots_adjust(top=0.90, bottom=0.05, wspace=0.3, hspace=0.2)

    return fig


def add_topics_to_df(
        items_by_topic: np.ndarray, dataset: pd.DataFrame, show_cols: List[str]
) -> pd.DataFrame:
    topic_cols = [f"topic_{i + 1}" for i in range(items_by_topic.shape[1])]

    dataset[topic_cols] = items_by_topic

    return dataset[[c for c in show_cols if c in dataset.columns] + topic_cols]


def add_topics_and_dates(
        items_by_topic: np.ndarray, dataset: pd.DataFrame,
) -> Optional[pd.DataFrame]:
    if len({'day', 'month', 'year'} - set(dataset.columns)) != 0:
        return None

    topic_cols = [f"topic_{i + 1}" for i in range(items_by_topic.shape[1])]
    dataset[topic_cols] = items_by_topic

    month_str_to_int = {
        'januari': 1, 'februari': 2, 'maart': 3, 'april': 4, 'mei': 5, 'juni': 6,
        'juli': 7, 'augustus': 8, 'september': 9, 'oktober': 10, 'november': 11, 'december': 12,
        'january': 1, 'february': 2, 'march': 3, 'may': 5, 'june': 6,
        'july': 7, 'august': 8, 'october': 10
    }

    dataset['year'] = pd.to_numeric(dataset['year'], errors='coerce', downcast='integer')
    dataset['month'] = dataset['month'].str.lower().replace(month_str_to_int)
    dataset['day'] = pd.to_numeric(dataset['day'], errors='ignore')

    dataset['month_year'] = pd.to_datetime(dataset[['month', 'year']].astype(str).agg(' '.join, axis=1),
                                           format='%m.0 %Y.0', errors='coerce')

    return dataset


def plot_total_documents_over_time(dataset: pd.DataFrame, granularity: str = 'month_year') -> plt.Figure:
    """
    Plot the total number of documents over time (as line plot).
    :param dataset: dataset containing the documents and a date column
    :param granularity: either `month_year`, `month` or `year`
    :return: figure with the line plot
    """
    date_counts = dataset.groupby(granularity).size()
    fig, ax = plt.subplots(figsize=(6, 2))
    date_counts.plot(kind='line', linewidth=0.7, marker='o', markersize=1, ax=ax)

    # set x-axis ticks for years
    if granularity == 'year':
        all_years = date_counts.index.sort_values()
        ax.set_xticks(all_years)
        ax.set_xticklabels([int(year) for year in all_years], rotation=45)

    ax.yaxis.set_major_locator(MaxNLocator(nbins=6, integer=True))
    ax.tick_params(axis='y', labelsize=6)
    ax.tick_params(axis='x', labelsize=6)

    ax.set_title(f'Total number of documents by {granularity}', fontsize=6)
    plt.xlabel(f'{granularity}', fontsize=6)
    plt.ylabel('Number of documents', fontsize=6)
    plt.grid(True)

    return fig


def plot_topic_propensity_over_time(dataset: pd.DataFrame) -> plt.Figure:
    """
    Create a subplot for every column in the dataset that starts with "topic_".
    :param dataset: DataFrame containing 'year' and topic columns starting with "topic_".
    :return: Figure with subplots for each "topic_" column.
    """
    # Filter columns that start with "topic_"
    topic_columns = [col for col in dataset.columns if col.startswith("topic_")]

    num_topics = len(topic_columns)
    fig, axes = plt.subplots(num_topics, 1, figsize=(5, 1.3 * num_topics), sharey=True)

    # Ensure axes is iterable even for a single subplot
    if num_topics == 1:
        axes = [axes]

    for ax, topic in zip(axes, topic_columns):
        date_counts = dataset.groupby('year')[topic].mean()
        date_counts.plot(kind='line', linewidth=0.7, marker='o', markersize=1, ax=ax)

        all_years = date_counts.index.sort_values()
        ax.set_xticks(all_years)
        ax.set_xticklabels([int(year) for year in all_years], rotation=45, fontsize=5)

        ax.set_title(f'{topic}', fontsize=6)
        ax.tick_params(axis='y', labelsize=5)
        ax.xaxis.label.set_visible(False)
        ax.grid(True, linestyle='--', linewidth=0.5, color='gray', alpha=0.7)

    plt.tight_layout()
    return fig
