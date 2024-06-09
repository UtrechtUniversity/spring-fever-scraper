import gensim
from gensim.utils import simple_preprocess
from gensim.corpora import Dictionary
from gensim.models import LdaModel


def main():
    #  Assuming 'corpus' is your list of documents
    corpus = [
        "document one content here",
        "document two content here",
        # more documents
    ]

    # Tokenize the documents
    tokenized_corpus = [simple_preprocess(doc) for doc in corpus]

    # Create a dictionary representation of the documents
    dictionary = Dictionary(tokenized_corpus)

    # Filter out extremes (optional)
    dictionary.filter_extremes(no_below=5, no_above=0.5)

    # Create a Bag-of-Words representation of the documents
    bow_corpus = [dictionary.doc2bow(doc) for doc in tokenized_corpus]

    # Set parameters
    num_topics = 10  # Number of topics you want to extract
    passes = 15  # Number of passes through the corpus during training

    # Train the LDA model
    lda_model = LdaModel(bow_corpus, num_topics=num_topics, id2word=dictionary, passes=passes)

    # Print the topics with their words
    for idx, topic in lda_model.print_topics(-1):
        print(f"Topic: {idx} \nWords: {topic}\n")

    # Get the topic distribution for each document
    # for i, doc_bow in enumerate(bow_corpus):
    #     print(f"Document {i}:")
    #     for index, score in sorted(lda_model[doc_bow], key=lambda tup: -1 * tup[1]):
    #         print(f"    Topic {index}: {score}")

    # import pyLDAvis
    # import pyLDAvis.gensim_models
    #
    # # Prepare the visualization
    # lda_vis = pyLDAvis.gensim_models.prepare(lda_model, bow_corpus, dictionary)
    #
    # # Display the visualization
    # pyLDAvis.show(lda_vis)


if __name__ == '__main__':
    main()