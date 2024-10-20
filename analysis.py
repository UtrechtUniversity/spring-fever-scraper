import pandas as pd
import streamlit as st

from analysis import MODELS, load_model
from analysis.visualize import plot_top_words, plot_topic_distribution


class Analysis:
    """
    Streamlit page for performing topic modeling analysis.
    """

    def __init__(self):
        self.uploaded_file = None
        self.dataset = None
        self.corpus = None
        self.model = None
        self.n_components = None
        self.n_features = None
        self.words_shown = None

    def __call__(self):
        st.title("Topic modelling analysis")

        with st.form("Configure topic model settings"):
            self.get_input()

            if st.form_submit_button("Run topic model"):
                if self.validate_clean_input():
                    self.run_analysis()

    def get_input(self):
        self.uploaded_file = st.file_uploader(
            "Dataset to analyze"
        )

        self.model = st.radio(
            "Model to use",
            list(MODELS.keys())
        )

        self.n_components = st.slider(
            "Number of topics to create",
            min_value=2, max_value=25, value=6
        )

        self.n_features = st.slider(
            "Number of words to consider",
            min_value=250, max_value=3000, step=250, value=1500
        )

        self.words_shown = st.slider(
            "Number of words to show in results",
            min_value=5, max_value=30, value=10
        )

    def validate_clean_input(self) -> bool:
        try:
            self.dataset = pd.read_csv(self.uploaded_file)
        except:
            st.error("Could not read file. Make sure it is a comma-separated .csv file.")
            return False

        if 'text' not in self.dataset.columns:
            st.error("File needs to contain a column called 'text'.")

        self.corpus = self.dataset['text'].astype(str).str.replace('user', '').str.replace('https', '').tolist()
        return True

    def run_analysis(self):
        st.subheader("Results")
        model = load_model(self.model, n_features=self.n_features, n_components=self.n_components)
        model.fit(self.corpus)

        fig = plot_top_words(model.words_by_topic, model.feature_names, n_top_words=self.words_shown)
        st.pyplot(fig)

        df = plot_topic_distribution(model.items_by_topic, self.dataset, 1)
        st.dataframe(df)


if __name__ == '__main__':
    st.set_page_config(layout="wide", page_title="Topic Modelling")
    Analysis()()
