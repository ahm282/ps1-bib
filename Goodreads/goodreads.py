# imports
import requests
from bs4 import BeautifulSoup
import json
import re

# init
books_titles = []
authors = []
cover_images = []

all_books = []
books_dict = dict()

url = "https://www.goodreads.com/shelf/show/booktok"
res = requests.get(url)  # bs4
soup = BeautifulSoup(res.text, "lxml")  # bs4
title_pattern = r"\s\((Paperback|Hardcover)\)"

google_api_key = "AIzaSyA-1NXifb5BScd-0zU3y8Z9DU5UQ-rgJIA"

# process
for book_title in soup.select(".bookTitle"):
    title = book_title.text.strip()
    corrected_title = re.sub(title_pattern, "", title, flags=re.IGNORECASE)  # Remove the words
    books_titles.append(corrected_title)

for author_name in soup.select(".authorName > span"):
    authors.append(author_name.text.strip())

# for book_cover in soup.select(".leftAlignedImage > img"):
#     cover_images.append(book_cover["src"])

# Google Books API to collect book covers
for title, author in zip(books_titles, authors):
    cover_image_url = "https://dummyimage.com/128x198/fff/000000.jpg&text=Image+not+found"  # Placeholder fallback
    query = f"intitle:{title}+inauthor:{author}"
    api_url = f"https://www.googleapis.com/books/v1/volumes?q={query}&key={google_api_key}"

    response = requests.get(api_url)
    data = response.json()

    if "items" in data:
        book_data = data["items"][0]  # Process first result
        if "volumeInfo" in book_data and "imageLinks" in book_data["volumeInfo"]:
            cover_image_url = book_data["volumeInfo"]["imageLinks"].get("thumbnail", cover_image_url)

    cover_images.append(cover_image_url)

for title, author, cover in zip(books_titles, authors, cover_images):
    all_books.append({"title": title, "author": author, "cover_url": cover})

    # next_page = soup.select_one(".c-pagination__link--nextprev--next")

    # if next_page != None:
    #     URL = "https://www.donner.nl" + next_page["href"]
    #     res = requests.get(URL)
    #     soup = BeautifulSoup(res.text, "lxml")
    # else:
    #     URL = None

books_dict = {"books":all_books}

# output
with open("goodreads.json", "w") as json_file:  # write to JSON
    json.dump(books_dict, json_file, indent=4)
