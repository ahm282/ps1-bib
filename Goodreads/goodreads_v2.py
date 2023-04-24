"""
This script collects book information from a Goodreads shelf and cover images from Google Books API.
The information collected includes: book titles (Goodreads), author names (Goodreads),
and cover images (Google Books API). The data collected is then saved in a JSON file.
Additionally, this script implements error handling and logging to keep track
of the information being processed.

Attributes:
    books_titles (list): A list to store book titles.
    authors (list): A list to store author names.
    cover_images (list): A list to store cover images.
    all_books (list): A list to store all books information.
    books_dict (dict): A dictionary to store all books information in JSON format.
    URL (str): A constant string representing the Goodreads shelf URL.
    FALLBACK_COVER (str): A constant string representing the default cover image URL.
    TITLE_PATTERN (str): A constant string representing the pattern for title correction.
    GOOGLE_API_KEY (str): A constant string representing the API key for Google Books API.

Exceptions:
    requests.exceptions.Timeout: Raised when a request to Goodreads or Google Books API times out.
    requests.exceptions.ConnectionError: Raised when a connection error occurs when
                                        making a request to Goodreads or Google Books API.
    requests.exceptions.RequestException: Raised when an unknown error occurs when
                                        making a request to Goodreads or Google Books API.
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
cover_images = []

all_books = []
books_dict = {}

# constants
URL = "https://www.goodreads.com/shelf/show/booktok"
FALLBACK_COVER = "https://dummyimage.com/128x198/fff/000000.jpg&text=Afbeelding+niet+gevonden"
TITLE_PATTERN = r"\s\((Paperback|Hardcover)\)"
GOOGLE_API_KEY = "AIzaSyA-1NXifb5BScd-0zU3y8Z9DU5UQ-rgJIA"

# process
# setup logging
logging.basicConfig(filename="goodreads.log", format='%(asctime)s %(levelname)-4s %(message)s',
                    level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')

try:
    # create the soup
    res = requests.get(URL, timeout=31)
    soup = BeautifulSoup(res.text, "lxml")

    # process the books
    for book_title in soup.select(".bookTitle"):
        book_title = book_title.text.strip()
        corrected_title = re.sub(TITLE_PATTERN, "", book_title, flags=re.IGNORECASE)
        books_titles.append(corrected_title)

    for author_name in soup.select(".authorName > span"):
        authors.append(author_name.text.strip())

    # Google Books API to collect book covers
    for title, author in zip(books_titles, authors):
        query = f"intitle:{title}+inauthor:{author}"
        api_url = f"https://www.googleapis.com/books/v1/volumes?q={query}&key={GOOGLE_API_KEY}"
        cover_image = ""

        try:
            response = requests.get(api_url, timeout=31)
            data = response.json()
            if "items" in data:
                book_data = data["items"][0]
                if "volumeInfo" in book_data and "imageLinks" in book_data["volumeInfo"]:
                    cover_image = book_data["volumeInfo"]["imageLinks"].get("thumbnail", FALLBACK_COVER)
                else:
                    cover_image = FALLBACK_COVER
            elif "error" in data:  # error 429 quota exceeded
                api_error = data["error"]
                logging.error(f"{api_error['code']}: {api_error['message']}")
                cover_image = FALLBACK_COVER

            cover_images.append(cover_image)

            # log book information
            logging.info(f"GOOGLE_BOOKS: {title} by {author}, Cover URL: {cover_image}")
        # log exceptions for debugging
        except requests.exceptions.Timeout as e:
            logging.error(f"Err_Requests: {e}")
        except requests.exceptions.ConnectionError as e:
            logging.error(f"Err_Requests: {e}")
        except requests.exceptions.RequestException as e:
            logging.error(f"Err_Requests: {e}")

    # create list of dictionaries
    for title, author, cover in zip(books_titles, authors, cover_images):
        all_books.append({"title": title, "author": author, "cover_url": cover})

    # JSON data
    books_dict = {"books": all_books}

    # write to JSON file
    with open("goodreads.json", "w", encoding="utf-8") as json_file:
        json.dump(books_dict, json_file, indent=4)
        logging.info("JSON: JSON file created succesfully")

# log exceptions for debugging
except requests.exceptions.Timeout as e:
    logging.error(f"Err_Requests: {e}")
except requests.exceptions.ConnectionError as e:
    logging.error(f"Err_Requests: {e}")
except requests.exceptions.RequestException as e:
    logging.error(f"Err_Requests: {e}")

end = time.perf_counter()
print(f"Time elapsed: {end - start:0.2f} seconds")
