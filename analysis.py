import hmac

import pandas as pd
import streamlit as st

from analysis import MODELS, load_model
from analysis.visualize import add_topics_and_dates, add_topics_to_df, plot_top_words, plot_topic_propensity_over_time, \
    plot_total_documents_over_time

SHOWN_COLS = ['title', 'source', 'date', 'original_text', 'page_name', 'url']
USE_PASSWORD = True


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
        st.title("Topic Modelling")

        if USE_PASSWORD and not self.check_password():
            st.stop()

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
            if 'url' in self.dataset.columns:
                self.dataset['url'] = self.dataset['url'].str.split(',').str[0]

        except:
            st.error("Could not read file. Make sure it is a comma-separated .csv file.")
            return False

        if 'text' not in self.dataset.columns:
            st.error("File needs to contain a column called 'text'.")
            return False

        self.corpus = self.dataset['text'].astype(str).str.replace('user', '').str.replace('https', '').tolist()
        return True

    def run_analysis(self):
        st.subheader("Results")

        with st.spinner("Applying model..."):
            model = load_model(self.model, n_features=self.n_features, n_components=self.n_components)
            model.fit(self.corpus)

        with st.spinner("Showing results..."):
            plot_words = plot_top_words(model.words_by_topic, model.feature_names, n_top_words=self.words_shown)
            st.pyplot(plot_words)

            combined_topics = add_topics_to_df(model.items_by_topic_normalized, self.dataset, SHOWN_COLS)
            st.data_editor(
                combined_topics,
                column_config={
                    "url": st.column_config.LinkColumn("Url"),
                } if 'url' in combined_topics.columns else {},
                use_container_width=True,
                disabled=True,
                hide_index=True
            )

            if (topics_and_dates := add_topics_and_dates(model.items_by_topic_normalized, self.dataset)) is not None:
                st.markdown("### Total number of documents by month & year")
                st.write("The discourse peaks each year in spring and explodes in the last few years.")
                plot_docs_over_time = plot_total_documents_over_time(topics_and_dates)
                st.pyplot(plot_docs_over_time, use_container_width=False)

                st.markdown("### Total number of documents by year")
                plot_docs_years = plot_total_documents_over_time(topics_and_dates, granularity='year')
                st.pyplot(plot_docs_years, use_container_width=False)

                st.markdown("### Total number of documents by month")
                st.write("The largest number of articles is published in March.")
                plot_docs_years = plot_total_documents_over_time(topics_and_dates, granularity='month')
                st.pyplot(plot_docs_years, use_container_width=False)

                st.markdown("### Mean propensity over time (years)")
                st.write("In the plot below, the average score of a topic across all articles is visualized.")
                plot_topic_scores = plot_topic_propensity_over_time(topics_and_dates)
                st.pyplot(plot_topic_scores, use_container_width=False)

    @staticmethod
    def check_password():

        def password_entered():
            if hmac.compare_digest(st.session_state["password"], st.secrets["password"]):
                st.session_state["password_correct"] = True
                del st.session_state["password"]  # Don't store the password.
            else:
                st.session_state["password_correct"] = False

        # Return True if the password is validated.
        if st.session_state.get("password_correct", False):
            return True

        # Show input for password.
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        if "password_correct" in st.session_state:
            st.error("😕 Password incorrect")
        return False


if __name__ == '__main__':
    st.set_page_config(layout="wide", page_title="Topic Modelling")
    Analysis()()
