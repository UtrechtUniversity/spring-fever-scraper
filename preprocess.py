from pathlib import Path

import pandas as pd
from confidence import load_name
from tqdm import tqdm

from preprocess import load_filereader, load_preprocessor
from preprocess.utils import group


def main():
    """
    Main script for preprocessing natural language. Loads data from file, applies preprocessing
    steps consecutively and stores data to csv and Excel. The files to load, as well as the
    steps to be applied, should be defined in `config/preprocess.yaml`.
    """
    config = load_name('config/preprocess').preprocess

    for input_file in tqdm(config.input_files, desc="Reading files to preprocess..."):
        reader = load_filereader(input_file.kind)

        documents = []

        for input_file_name in input_file.filenames:
            file_name = Path(input_file_name)
            documents.append(reader(file_name))

        documents = pd.concat(documents)

        if input_file.group_by:
            documents = group(documents, list(input_file.group_by))

        documents['original_text'] = documents['text']

        for step in tqdm(config.steps, desc="    Applying preprocessing steps..."):
            preprocessor = load_preprocessor(step.kind, **step.settings)
            documents['text'] = documents['text'].apply(preprocessor)

        documents.to_csv(f"{input_file.name}_preprocessed.csv", index=False)
        documents.to_excel(f"{input_file.stem}_preprocessed.xlsx", index=False)


if __name__ == '__main__':
    main()
