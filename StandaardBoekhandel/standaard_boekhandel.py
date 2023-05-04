"""
This script collects book information from a Donner.nl shelf and cover images from Google Books API.
The information collected includes: book titles (Donner.nl), author names (Donner.nl),
and cover images (Google Books API). The data collected is then saved in a JSON file.
Additionally, this script implements error handling and logging to keep track
of the information being processed.

Attributes:
    books_titles (list): A list to store book titles.
    authors (list): A list to store author names.
    all_books (list): A list to store all books information.
    books_dict (dict): A dictionary to store all books information in JSON format.
    URL (str): A constant string representing the Donner.nl shelf URL.
    TITLE_PATTERN (str): A constant string representing the pattern for title correction.

Exceptions:
    requests.exceptions: Raised when a request to Donner.nl times out.
"""

# imports
import time
start = time.perf_counter()

import logging
import json
import re
import requests
from bs4 import BeautifulSoup


# init

# variables
books_titles = []
authors = []
all_books = []
books_dict = {}

# constants
URL = "https://www.standaardboekhandel.be/c/boeken-ff70aa56/bekend-van-tiktok?filter=OrderableSB.eq.true&page=12&page_size=24&sort=RelevanceSb&sort_type=desc&view_size=288"
TITLE_PATTERN = r"\s\((Paperback|Hardcover)\)"

# process

# setup logging
logging.basicConfig(filename="standaard_boekhandel.log", format='%(asctime)s %(levelname)-4s %(message)s',
                    level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')

try:
    # create the soup
    res = requests.get(URL, timeout=31)
    soup = BeautifulSoup(res.text, "lxml")

    # process the books
    for book_title in soup.select(".c-product__title"):
        book_title = book_title.text.strip()
        corrected_title = re.sub(TITLE_PATTERN, "", book_title, flags=re.IGNORECASE)
        books_titles.append(corrected_title)

    for author_name in soup.select(".c-product__subtitle > a"):
        authors.append(author_name.text.strip())

    for title, author in zip(books_titles, authors):
        all_books.append({"title": title, "author": author})

    # JSON data
    books_dict = {"books": all_books}

    # write to JSON file
    with open("standaard_boekhandel.json", "w", encoding="utf-8") as json_file:
        json.dump(books_dict, json_file, indent=4)
        logging.info("JSON: JSON file created succesfully")

# log exceptions for debugging
except requests.exceptions as e:
    logging.error(f"Err_Requests: {e}")

end = time.perf_counter()
print(f"Time elapsed: {end - start:0.2f} seconds")
