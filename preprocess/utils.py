import csv
from pathlib import Path
from typing import Any, Dict, List
import zipfile
import os

import pandas as pd

from striprtf.striprtf import rtf_to_text


def read_from_csv(filename: os.PathLike) -> pd.DataFrame:
    return pd.read_csv(filename).astype('str')


def read_from_zip(zip_file_path: os.PathLike) -> pd.DataFrame:
    zip_path = Path(zip_file_path)
    output_dir = zip_path.parent / zip_path.stem
    os.makedirs(output_dir, exist_ok=True)

    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(output_dir)

    parsed_rtfs = []
    for root, _, files in os.walk(output_dir):
        for file in files:
            if file.endswith('.rtf'):
                rtf_file_path = os.path.join(root, file)
                with open(file, 'r') as rtf_file:
                    rtf_content = rtf_file.read()
                    try:
                        text = rtf_to_text(rtf_content)
                    except Exception as e:
                        print(f"Error extracting text from {rtf_file_path}: {e}")
                        continue
                    parsed_rtfs.append(parse_rtf(text))

    return pd.DataFrame(parsed_rtfs)


def parse_rtf(rtf_text: str) -> Dict[str, str]:
    text_split = rtf_text.split("\n")
    # TODO


def to_csv(documents: List[Dict[str, Any]], original_filename: os.PathLike) -> None:
    new_filename = f"{Path(original_filename).root}_preprocessed.csv"
    with open(new_filename, "w", encoding='utf-8', newline="") as csvfile:
        writer = csv.DictWriter(csvfile)
        writer.writeheader(documents[0].keys)
        writer.writerows(documents)