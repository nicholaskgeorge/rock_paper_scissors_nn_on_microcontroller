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
    """URLs may contain information on what the webpage is about. This function
    parses a URL to extract the "title" of a webpage, which is returned as a string.
    We will use this function to parse URLs from the GDELT database.

    Args:
        url (str): a URL

    Returns:
        str: the title of the webpage

    Note the following requirements:

    - A URL is contains segments separated by "/". The segment of interest in the one with
    3 or more dashes ("-") in the text as that is likely to contain the title of the webpage.
    For brevity, we will refer to this segment as "the segment".

    - If there are multiple segments with more than three dashes, "the segment" is furthest segment
    from the root of the URL. For example, in the URL "https://{1}/{2}/{3}/{4}", the furthest segment is "4".

    - If there are no segments with at least three dashes, return None.

    - The segment must have fewer than 8 digits (< 8).

    - Dashes in the segment are replaced with spaces.

    - "Words" in the segment with six or more digits are removed.
       Example:
       "A999999" is removed.
       "A99999" is kept.

    - Words in the segment are separated by a single space.

    - Replace ".cms" and ".html" in the string to ""

    - The return string is in lowercase.

    - The return string does not contain the following characters at the beginning or end of the string:
      " ", "/", ".". In other words, there are no leading or trailing spaces, slashes, or full stops

    - In an edge case where the segment is an empty string, return None.


    Here are some examples:

    1. https://www.yahoo.com/news/russian-military-convoy-blocked-entering.html
    -> return "russian military convoy blocked entering"

    2. https://www.yahoo.com/news/russian-military-convoy-blocked-entering-12345678.html
    -> return None because the segment contains 8 or more digits

    3. https://www.den-ver-post.com/2025/02/11/king-soopers-union-strike-lawsuit-restraining-order-A999999/
    -> return "king soopers union strike lawsuit restraining order"

    4. https://www.yahoo.com/news/russian---military--convoy-blocked-entering.html
    -> return "russian military convoy blocked entering"

    """

    page_title = None

    ##############################################################################
    # TODO: Implement your code here
    ##############################################################################

    pass

    ##############################################################################
    return page_title


def read_gdelt(data_folder: str, filename: str) -> pd.DataFrame:
    """
    Given a raw CSV file, create a dataframe with the following characteristics:

    1. Set GLOBALEVENTID (str) as the index of the dataframe.

    2. Contains the following columns: SQLDATE (str), EventCode (int), QuadClass (int), GoldsteinScale (float),
    ActionGeo_FullName (str), and SOURCEURL (str).
    Hint: You might find a constant in helpers.py useful.

    3. A new column called Text, which contains information parsed from the SOURCEURL column.

    4. Remove rows with missing or None values.

    5. Remove rows with duplicated SOURCEURL. If multiple rows share the same SOURCEURL,
    keep the row with the smallest GLOBALEVENTID.

    Args:
        data_folder (str): the folder containing the file
        filename (str): the name of the file to read

    Returns:
        pd.DataFrame, the cleaned dataframe

    """
    df = pd.DataFrame()
    ##############################################################################
    # TODO: Implement your code here
    ##############################################################################
    # Hint: the resulting df should have 7 columns.
    # Hint: Do GDELT files contain a header row?

    pass

    ##############################################################################

    return df
