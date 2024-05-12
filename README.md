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

Anonymization occurs by replacing usernames by an integer (e.g. "@JohnDoe" becomes "@0", "@JaneDoe" becomes "@1").
This is done by first collecting all author usernames of all posts, and then replacing these in the texts of the posts themselves.
This approach has the limitation that usernames which are *mentioned in* posts, but who are never the *author of* a post, are not recognized as usernames and therefore not replaced.
Therefore, if privacy is of concern (which it most likely is), make sure to perform a manual check of the retrieved data before further processing.

## Preprocessing

The script `preprocess.py` contains functionality for preprocessing of natural language. 

TODO 

## Contact

A publication about the results of the analysis performed on the basis of the data scraped is forthcoming (and will be linked here).
Otherwise, this repository will no longer be actively maintained.
Should you nonetheless wish to get in touch, you may do so by opening an Issue.