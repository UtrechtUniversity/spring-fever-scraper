import pandas as pd
from confidence import load_name
from tqdm import tqdm

from preprocess import load_preprocessor


def main():
    """
    Main script for preprocessing natural language. Loads data from csv, applies preprocessing
    steps consecutively and stores data to csv again. The csv file to load, as well as the
    steps to be applied, should be defined in `config/preprocess.yaml`. Requires that the
    csv file has a column named 'text' (to which the preprocessing will be applied).
    """
    config = load_name('config/preprocess')

    df = pd.read_csv(config.preprocess.input_file).astype('str')
    df['original_text'] = df['text']
    for step in tqdm(config.preprocess.steps, desc="Applying preprocessing steps..."):
        preprocessor = load_preprocessor(step.kind, **step.settings)
        df['text'] = df['text'].apply(preprocessor)

    df.to_csv("scratch/preprocessed.csv", index=False)


if __name__ == '__main__':
    main()
