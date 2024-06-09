from confidence import load_name
from tqdm import tqdm

from preprocess import load_filereader, load_preprocessor, to_csv


def main():
    """
    Main script for preprocessing natural language. Loads data from file, applies preprocessing
    steps consecutively and stores data to csv again. The files to load, as well as the
    steps to be applied, should be defined in `config/preprocess.yaml`.
    """
    config = load_name('config/preprocess')
    for input_file in tqdm(config.input_files, desc="Reading files to preprocess..."):
        reader = load_filereader(input_file.kind)
        preprocessed = []
        for file_name in input_file.names:
            documents = reader(file_name)
            for doc in tqdm(documents, desc="Preprocessing documents in file..."):
                doc['original_text'] = doc['text']
                for step in config.preprocess.steps:
                    preprocessor = load_preprocessor(step.kind, **step.settings)
                    doc['text'] = preprocessor(doc['text'])
        to_csv(preprocessed, input_file.name)


if __name__ == '__main__':
    main()
