import csv
import os
from pathlib import Path
from typing import Any, Dict, Generator, List


def read_from_csv(filename: os.PathLike) -> Generator[List[Any], None, None]:
    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile)
        # TODO check columns
        yield from reader

def read_from_zip(filename: os.PathLike) -> Generator[List[Any], None, None]:
    pass


def to_csv(documents: List[Dict[str, Any]], original_filename: os.PathLike) -> None:
    new_filename = f"{Path(original_filename).root}_preprocessed.csv"
    with open(new_filename, "w", encoding='utf-8', newline="") as csvfile:
        writer = csv.DictWriter(csvfile)
        writer.writeheader(documents[0].keys)
        writer.writerows(documents)