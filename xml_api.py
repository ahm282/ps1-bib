import requests
import xml.etree.ElementTree as ET
import json

# Book info list
books = []
books_dict = dict()
book_titles = []  # keep track of book titles

# load scraped books from generated JSON file
with open("./StandaardBoekhandel/standaard_boekhandel.json") as json_file:
    data = json.load(json_file)

# Get info from Cultuurconnect API
for book in data['books']:
    # Define the API endpoint and parameters
    url = "http://antwerpen.staging.aquabrowser.be/api/v1/search/"
    params = {
        "q": book['title'],
        "authorization": "629e87cf5fe7767339231c6e0e1307ec",
        "refine": "true",
        "facet": "Format(Book)",
        "lang": "nl",
        "detaillevel": "basic",
        "pagesize": "1",
        "s": "cover"
    }

    # Send the request and get the response
    response = requests.get(url, params=params)

    # Parse XML response
    root = ET.fromstring(response.content)

    # Extract info
    for child in root:
        if child.tag == 'results':
            for result in child.iter('result'):
                book = {}

                # Title and author
                title_elem = result.find('titles/title')
                author_elem = result.find('authors/main-author')
                if title_elem is not None and author_elem is not None:
                    book_title = title_elem.text
                    if book_title not in book_titles:  # check if book is not a duplicate
                        book_titles.append(book_title)  # add title to the list of added books
                        book['title'] = book_title
                        book['author'] = author_elem.text

                        # Genre
                        genre_elem = result.find('genres/genre')
                        if genre_elem is not None:
                            book['genre'] = genre_elem.text
                        else:
                            book['genre'] = None

                        # Number of pages
                        pages_elem = result.find('description/number-of-pages')
                        if pages_elem is not None:
                            book['pages'] = int(pages_elem.text)

                        # Summary
                        summary_elem = result.find('summaries/summary')
                        if summary_elem is not None:
                            book['summary'] = summary_elem.text

                        # Language
                        language_elem = result.find('languages/language')
                        if language_elem is not None:
                            book['language'] = language_elem.text

                        # Publication date
                        pub_elem = result.find('publication/year')
                        if pub_elem is not None:
                            book['publication_date'] = pub_elem.text

                        # Series
                        series_elem = result.find('series/series-title')
                        if series_elem is not None:
                            book['series'] = series_elem.text
                        else:
                            book['series'] = "no"

                        # Cover image URL
                        cover_elem = result.find('coverimages/coverimage')
                        if cover_elem is not None:
                            # original URL
                            cover_image_url = cover_elem.text

                            # modify URL to use "large" size
                            large_cover_image_url = cover_image_url.replace("coversize=small", "coversize=large")

                            # Add cover to book
                            book['cover_image'] = large_cover_image_url

                        books.append(book)

books_dict["books"] = books

with open('./website/api_books.json', 'w') as f:
    json.dump(books_dict, f, indent=4)
