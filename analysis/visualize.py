import locale
import math
from typing import Iterable, List, Optional

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt


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
    fig, axes = plt.subplots(2, int(math.ceil(words_by_topic.shape[0] / 2)), figsize=(30, 15), sharex=True)
    axes = axes.flatten()
    for topic_idx, topic in enumerate(words_by_topic):
        top_features_ind = topic.argsort()[-n_top_words:]
        top_features = feature_names[top_features_ind]
        weights = topic[top_features_ind]

        ax = axes[topic_idx]
        ax.barh(top_features, weights, height=0.7)
        ax.set_title(f"Topic {topic_idx + 1}", fontdict={"fontsize": 30})
        ax.tick_params(axis="both", which="major", labelsize=20)
        for i in "top right left".split():
            ax.spines[i].set_visible(False)

    plt.subplots_adjust(top=0.90, bottom=0.05, wspace=0.90, hspace=0.3)

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

    locale.setlocale(locale.LC_TIME, 'nl_NL.UTF-8')

    dataset['month_year'] = pd.to_datetime(dataset[['month', 'year']].astype(str).agg(' '.join, axis=1),
                                           format='%B %Y.0', errors='coerce')

    dataset['year'] = pd.to_numeric(dataset['year'], errors='coerce', downcast='integer')

    return dataset


def plot_total_documents_over_time(dataset: pd.DataFrame, granularity: str = 'month_year') -> plt.Figure:
    """
    Plot the total number of documents over time (as line plot).
    :param dataset: dataset containing the documents and a date column
    :param granularity: either `month_year` or `year`
    :return: figure with the line plot
    """
    date_counts = dataset.groupby(granularity).size()
    fig, ax = plt.subplots(figsize=(6, 2))
    date_counts.plot(kind='line', marker='o', markersize=1, ax=ax)

    # set x-axis ticks for years
    if granularity == 'year':
        all_years = date_counts.index.sort_values()
        ax.set_xticks(all_years)
        ax.set_xticklabels([int(year) for year in all_years], rotation=45, fontsize=8)

    ax.set_title(f'Total number of documents by {granularity}')
    plt.xlabel(f'{granularity}')
    plt.ylabel('Number of documents')
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
    fig, axes = plt.subplots(num_topics, 1, figsize=(5, 1 * num_topics), sharex=True, sharey=True)

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
        ax.set_xlabel('year', fontsize=6)
        ax.tick_params(axis='y', labelsize=5)
        ax.grid(True, linestyle='--', linewidth=0.5, color='gray', alpha=0.7)

    fig.text(0.01, 0.5, 'Average Propensity', va='center', rotation='vertical', fontsize=6)

    plt.tight_layout()
    return fig
