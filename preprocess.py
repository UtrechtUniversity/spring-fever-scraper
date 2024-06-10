from pathlib import Path

from confidence import load_name
from tqdm import tqdm

from preprocess import load_filereader, load_preprocessor


def main():
    """
    Main script for preprocessing natural language. Loads data from file, applies preprocessing
    steps consecutively and stores data to csv and Excel. The files to load, as well as the
    steps to be applied, should be defined in `config/preprocess.yaml`.
    """
    config = load_name('config/preprocess').preprocess

    for input_file in tqdm(config.input_files, desc="Reading files to preprocess..."):
        reader = load_filereader(input_file.kind)

        for input_file_name in input_file.names:
            file_name = Path(input_file_name)
            documents = reader(file_name)
            documents['original_text'] = documents['text']

            for step in tqdm(config.steps, desc="    Applying preprocessing steps..."):
                preprocessor = load_preprocessor(step.kind, **step.settings)
                documents['text'] = documents['text'].apply(preprocessor)

            documents.to_csv(file_name.parent / f"{file_name.stem}_preprocessed.csv", index=False)
            documents.to_excel(file_name.parent / f"{file_name.stem}_preprocessed.xlsx", index=False)


if __name__ == '__main__':
    main()
