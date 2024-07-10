import os
import re
import zipfile
from pathlib import Path
from typing import Dict, Optional, Sequence, Tuple

import pandas as pd
from striprtf.striprtf import rtf_to_text

DATE_PATTERN_1 = r"(\d{1,2})\s(\w+)\s(\d{4})"
DATE_PATTERN_2 = r"(\b\w+\b)\s(\d{1,2}),\s(\d{4})"
REMOVE_TEXTS = ["ABSTRACT ", "SAMENVATTING ", "VOLLEDIGE TEKST: "]


def read_from_csv(filename: os.PathLike) -> pd.DataFrame:
    return pd.read_csv(filename).astype('str')


def read_from_zip(zip_file_path: os.PathLike) -> pd.DataFrame:
    zip_path = Path(zip_file_path)
    output_dir = zip_path.parent / zip_path.stem
    os.makedirs(output_dir, exist_ok=True)

    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(output_dir)

    parsed_rtfs = []
    rtf_files = [f for f in os.listdir(output_dir)
                 if f.endswith('.rtf') and not '_doclist' in f]
    for file in rtf_files:
        with open(output_dir / file, 'r') as rtf_file:
            rtf_content = rtf_file.read()
            try:
                text = rtf_to_text(rtf_content)
            except Exception as e:
                print(f"Error extracting text from {file}: {e}")
                continue
            parsed_rtfs.append(parse_rtf(text))

    return pd.DataFrame(parsed_rtfs)


def parse_rtf(
        rtf_text: str,
        start_text: Optional[str] = 'Body',
        end_text: Optional[str] = 'Classification'
) -> Dict[str, str]:
    text_split = [" ".join(text.split()) for text in rtf_text.split("\n") if text]
    title = text_split[0]
    source = text_split[1]
    date = text_split[2]

    content_start = text_split.index(start_text) + 1 if start_text in text_split else 0
    content_end = text_split.index(end_text) if end_text in text_split else len(text_split)

    text = " ".join(text_split[content_start:content_end])

    for remove_text in REMOVE_TEXTS:
        text = text.replace(remove_text, "")

    day, month, year = parse_date(date)

    return {
        'title': title,
        'source': source,
        'day': day,
        'month': month,
        'year': year,
        'date': date,
        'text': text
    }


def parse_date(date: str) -> Tuple[Optional[int], Optional[int], Optional[int]]:
    match1 = re.search(DATE_PATTERN_1, date)
    if match1:
        day, month, year = match1.groups()
        return day, month, year

    match2 = re.search(DATE_PATTERN_2, date)
    if match2:
        month, day, year = match2.groups()
        return day, month, year

    return None, None, None


def group(df: pd.DataFrame, columns: Sequence[str]) -> pd.DataFrame:
    new_df = df.groupby(columns).agg(lambda x: ", ".join(str(i) for i in x if i)).reset_index()
    return new_df
