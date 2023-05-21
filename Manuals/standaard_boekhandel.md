## "standaard_boekhandel.py"

1. Ensure you have Python installed on your system (Python 3.6 or above).
2. Import the required libraries at the beginning of the script:

```
import logging
import json
import re
import requests
from bs4 import BeautifulSoup
```

3. Initialize the variables and constants

```
books_titles = []
authors = []
all_books = []
books_dict = {}
URL = "https://www.standaardboekhandel.be/c/boeken-ff70aa56/bekend-van-tiktok?filter=OrderableSB.eq.true&page=12&page_size=24&sort=RelevanceSb&sort_type=desc&view_size=288"
TITLE_PATTERN = r"\s\((Paperback|Hardcover)\)"
```

4. Set up logging to track the information being processed

```
logging.basicConfig(filename="standaard_boekhandel.log", format='%(asctime)s %(levelname)-4s %(message)s',
                    level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')
```

5. Wrap the script's main logic in a try-except block to handle exceptions and log them
6. create a BeautifulSoup object by making a request to the Standaard-Boekhandel URL

```
res = requests.get(URL, timeout=31)
soup = BeautifulSoup(res.text, "lxml")
```

7. Process the books' information by extracting the book titles and authors from the HTML using CSS selectors:

```
for book_title in soup.select(".c-product__title"):
    book_title = book_title.text.strip()
    corrected_title = re.sub(TITLE_PATTERN, "", book_title, flags=re.IGNORECASE)
    books_titles.append(corrected_title)

for author_name in soup.select(".c-product__subtitle > a"):
    authors.append(author_name.text.strip())
```

8. Combine the book titles and authors into a list of dictionaries, where each dictionary represents a book:

```
for title, author in zip(books_titles, authors):
    all_books.append({"title": title, "author": author})
```

9. Create a dictionary that contains all the book information
10. Write the book information to a JSON file
