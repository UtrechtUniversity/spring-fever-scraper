# uu-spring-fever-scraper
This repository contains tools for scraping and analyzing natural language content related to the *Spring Fever week (Lentekriebels)*.
The tools developed are intended for academic research purposes.
This repository was created for a research project initiated by Utrecht University.

## Getting started

### Prerequisites

- Python 3.10 or newer

### Requirements
All package requirements for running the application are specified in `requirements.txt`. Packages can be installed from PyPi, e.g. through `pip install -r requirements.txt`.

## Scraper

The script `scrape.py` can be used for scraping web pages.
The scrapers retrieve posts by individual authors/accounts on the web page.
The anonymized author of the post, as well as the text of the post, are retrieved and exported to a csv file.

Currently, scrapers have been developed for websites which contain content relevant to the Lentekriebels week.
These are:
* Facebook (comments for any given post)
* YouTube (comments for any given video) 
* www.ouders.nl (responses to any given forum post)

The web pages of interest for the present research project are defined in `config/scrape.yaml`, but the scrapers may be used for any page on these websites.
In addition, the repository is set up such that it can be readily extended to be used for scraping other websites.

If the Facebook or YouTube scraper are used, make sure that you provide the appropriate credentials (cookies or API key respectively).
See `scraper/facebook.py` and `scraper/youtube.py` for specifics.

As is common, the developed scrapers rely on the existing page layout of the websites at the time of development. If the structure of these pages should change, the scrapers may no longer work.

**Anonymization** occurs by replacing usernames by an integer (e.g. `@JohnDoe` becomes `@0`, `@JaneDoe` becomes `@1`).
This is done by first collecting all author usernames of all posts and assigning them an integer, and then replacing all occurrences of a username in the texts of the posts by its assigned integer.
This approach has the limitation that usernames which are *mentioned in* posts, but who are never the *author of* a post, are not recognized as usernames and therefore not replaced.
Therefore, if privacy is of concern (which it most likely is), make sure to perform a manual check of the retrieved data before further processing.

## Preprocessing

The script `preprocess.py` contains functionality for preprocessing of natural language.
The available options were developed with classical topic modelling approaches in mind.
For topic modelling, it is desirable that documents are "normalized" as much as possible, in order to increase the density of the distribution of the model to be fit.
This means that all preprocessing options help to reduce the text to a form that maintains the most important features that capture the meaning of the text, while removing as much redundancy as possible.
Moreover, the documents are assumed to be in Dutch, so Dutch lexicons are used wherever appropriate (although it should be straightforward to replace these if required).

The preprocessing options that can be executed are listed below.

* **Account masking**: following the anonymization described above, documents can be normalized by replacing all of `@0`, `@1`, `@2`, ... etc. with `@USER`.
* **Stopword removal**: removes all stopwords that are included in the NLTK Dutch stopword corpus.
* **Punctuation removal**: removes all punctuation according to Python's `string.punctuation`, that is, the following characters: `!"#$%&'()*+, -./:;<=>?@[\]^_`{|}~`
* **Lemmatization**: reduces words to a root form, using the `nl_core_news_lg` corpus from Spacy.
* **Stemming**: reduces words to their stem, e.g. by removing prefixes and suffixes, using the Dutch `snowball` stemmer from Spacy. Lemmatization seems to perform better than stemming for the present corpus.

The preprocessing steps to be executed are defined in `config/preprocess.yaml`.
The steps are applied in the order that they are listed.
In addition, the files that preprocessing should be applied to are listed in the same `.yaml` file.

**Note**: if you want to run lemmatization, run `python -m spacy download nl_core_news_lg` before running `preprocess.py`.

## Contact

A publication about the results of the analysis performed on the basis of the data scraped using this repository is forthcoming (and will be linked here).
Otherwise, this repository will no longer be actively maintained.
Should you nonetheless wish to get in touch, you may do so by opening an Issue.