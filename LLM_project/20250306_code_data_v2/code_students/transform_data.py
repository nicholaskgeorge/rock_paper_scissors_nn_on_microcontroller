"""transform_data.py: Contains functions for run_vector_database.py.

Copyright 2025, Cornell University

Cornell University asserts copyright ownership of this template and all derivative
works, including solutions to the projects assigned in this course. Students
and other users of this template code are advised not to share it with others
or to make it available on publicly viewable websites including online repositories
such as Github.

Sharing solutions with current or future students of ENMGT5400 is
prohibited and subject to being investigated as a Code of Academic Integrity violation.

-----do not edit anything above this line---
"""

import os

import pandas as pd


def parse_url(url: str) -> str:
    """Parses a URL to extract the "title" of a webpage based on specific rules.
    
    Args:
        url (str): a URL.
        
    Returns:
        str: the title of the webpage or None if no valid title is found.
    """
    # Split the URL into segments using '/' as the delimiter.
    segments = url.split('/')
    
    # Identify segments that contain at least 3 dashes.
    candidate_segments = [seg for seg in segments if seg.count('-') >= 3]
    if not candidate_segments:
        return None
    
    # Select the furthest segment from the root (last candidate).
    segment = candidate_segments[-1]
    
    # Remove '.cms' and '.html' substrings from the segment.
    segment = segment.replace(".cms", "").replace(".html", "")
    
    # If the segment becomes empty after removals, return None.
    if not segment:
        return None
    
    # Check overall digit count in the segment; must be fewer than 8.
    total_digits = sum(1 for char in segment if char.isdigit())
    if total_digits >= 8:
        return None
    
    # Replace all dashes with spaces.
    segment = segment.replace('-', ' ')
    
    # Split the segment into words (automatically handles multiple spaces).
    words = segment.split()
    
    # Remove words that contain six or more digits.
    cleaned_words = []
    for word in words:
        digit_count = sum(1 for ch in word if ch.isdigit())
        if digit_count >= 6:
            continue
        cleaned_words.append(word)
    
    # Join the words with a single space.
    result = ' '.join(cleaned_words)
    
    # Convert to lowercase.
    result = result.lower()
    
    # Remove leading or trailing spaces, slashes, or periods.
    result = result.strip(" /.")
    
    # If the result is empty after processing, return None.
    if not result:
        return None
    
    return result

import pandas as pd
import os
from typing import Dict, Any

# Constants that might be in helpers.py
# Based on the test file's expectations for column positions
GDELT_COLUMNS = {
    0: 'GLOBALEVENTID',
    1: 'SQLDATE',
    26: 'EventCode', 
    29: 'QuadClass',
    30: 'GoldsteinScale',
    37: 'ActionGeo_FullName',
    57: 'SOURCEURL'
}


import os
import pandas as pd

def read_gdelt(data_folder: str, filename: str) -> pd.DataFrame:
    """
    Given a raw CSV file (without headers), create a dataframe with the following characteristics:

    1. Set GLOBALEVENTID (str) as the index of the dataframe.
    2. Contains the following columns (with proper types): 
       SQLDATE (str), EventCode (int), QuadClass (int), GoldsteinScale (float),
       ActionGeo_FullName (str), and SOURCEURL (str).
    3. A new column called Text, which contains information parsed from the SOURCEURL column.
    4. Remove rows with missing or None values.
    5. Remove rows with duplicated SOURCEURL. If multiple rows share the same SOURCEURL,
       keep the row with the smallest GLOBALEVENTID.

    Args:
        data_folder (str): the folder containing the file.
        filename (str): the name of the file to read.

    Returns:
        pd.DataFrame: the cleaned dataframe.
    """
    # Construct the full file path.
    filepath = os.path.join(data_folder, filename)
    
    # Read the CSV file with no header; the file is tab-separated.
    df_raw = pd.read_csv(filepath, sep="\t", header=None, engine='python')
    
    # Based on the GDELT format, select the required columns by their positions:
    # 0: GLOBALEVENTID, 1: SQLDATE, 26: EventCode, 29: QuadClass, 30: GoldsteinScale,
    # 50: ActionGeo_FullName, 57: SOURCEURL.
    df = pd.DataFrame({
        "GLOBALEVENTID": df_raw.iloc[:, 0],
        "SQLDATE": df_raw.iloc[:, 1],
        "EventCode": df_raw.iloc[:, 26],
        "QuadClass": df_raw.iloc[:, 29],
        "GoldsteinScale": df_raw.iloc[:, 30],
        "ActionGeo_FullName": df_raw.iloc[:, 50],
        "SOURCEURL": df_raw.iloc[:, 57]
    })
    
    # Convert columns to appropriate types.
    df["SQLDATE"] = df["SQLDATE"].astype(str)
    df["EventCode"] = df["EventCode"].astype(int)
    df["QuadClass"] = df["QuadClass"].astype(int)
    df["GoldsteinScale"] = df["GoldsteinScale"].astype(float)
    df["ActionGeo_FullName"] = df["ActionGeo_FullName"].astype(str)
    df["SOURCEURL"] = df["SOURCEURL"].astype(str)
    
    # Create the new 'Text' column by parsing the SOURCEURL.
    # Assumes that the function parse_url(url: str) -> str is defined in the same module.
    df["Text"] = df["SOURCEURL"].apply(parse_url)
    
    # Remove rows with any missing or None values.
    df = df.dropna()
    
    # Remove duplicate SOURCEURL rows:
    # Convert GLOBALEVENTID to int for numerical sorting and deduplication.
    df["GLOBALEVENTID_int"] = df["GLOBALEVENTID"].astype(int)
    df = df.sort_values(by="GLOBALEVENTID_int")
    df = df.drop_duplicates(subset="SOURCEURL", keep="first")
    df = df.drop(columns=["GLOBALEVENTID_int"])
    
    # Set GLOBALEVENTID (as string) as the index.
    df = df.set_index("GLOBALEVENTID")
    
    return df

# Example usage:
if __name__ == "__main__":
    # Update these paths as needed.
    data_folder = "path/to/data_folder"
    filename = "20250212.export.CSV"
    
    # Ensure that the parse_url function is defined in this module.
    df_cleaned = read_gdelt(data_folder, filename)
    print(df_cleaned.head())


