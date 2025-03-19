""" download_data.py: Simulate scraping data from the GDELT project.

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

import requests
from bs4 import BeautifulSoup
import re


def list_gdelt_files(year: int = 2024) -> dict:
    """
    This function visits the website: http://data.gdeltproject.org/events/, then
    returns a dict containing information on available GDELT files with the following format:

    {
    date1 (str): {
        "md5": str,
        "filesize": str,
        "url": "str",
    date2 (str): {
        "md5": str,
        "filesize": str,
        "url": "str",
    .
    .
    .
    dateX (str): {
        "md5": str,
        "filesize": str,
        "url": "str",
    }

    Args:
        year (int): The year to filter the files.

    Returns:
        dict: A dictionary containing information of available files from the year.

    Note the following:
    - DO NOT download the files. Just list them.
    - The dates should be in the format "YYYYMMDD" (e.g., "20240101").
    - The "md5" key should contain the MD5 hash of the file, e.g. "fdb34326d00aba8fef3d987fb3dfa145".

    """

    url = "http://data.gdeltproject.org/events/"
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch data from {url}")

    soup = BeautifulSoup(response.content, 'html.parser')
    files = soup.find_all('a', href=True)

    output = {}

    for file in files:
        file_url = file['href']
        if file_url.endswith('.export.CSV.zip') and str(year) in file_url:
            date_match = re.search(r'\d{8}', file_url)
            if date_match:
                date = date_match.group(0)
                # Extract MD5 and filesize from the adjacent text or attributes
                md5_match = re.search(r'MD5: ([a-fA-F0-9]{32})', file.parent.text)
                filesize_match = re.search(r'\((\d+\.\d+)MB\)', file.parent.text)
                md5 = md5_match.group(1) if md5_match else "unknown_md5"
                filesize = filesize_match.group(1) if filesize_match else "0"
                output[date] = {
                    "md5": md5,
                    "filesize": filesize,
                    "url": url + file_url
                }

    return output
