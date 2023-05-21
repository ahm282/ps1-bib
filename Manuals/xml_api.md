## "XML_API.py"

1. Ensure you have Python installed on your system (Python 3.6 or above).
2. Import the required libraries at the beginning of the script:

```
import requests
import xml.etree.ElementTree as ET
import json
import os
```

3. Define the variables and data structures needed to store the book information:

```
books = []
books_dict = dict()
book_titles = []
```

4. Load the scraped books from the generated JSON file:

```
with open("./StandaardBoekhandel/standaard_boekhandel.json") as json_file:
    data = json.load(json_file)
```

5. The CultuurConnectAPI uses **XML**. Implement needed logic to retrieve data.

```
url = "http://antwerpen.staging.aquabrowser.be/api/v1/search/"
    params = {
        "q": book['title'],
        "authorization": os.getenv("API_KEY"),
        "refine": "true",
        "facet": "Format(Book)",
        "lang": "nl",
        "pagesize": "1",
        "s": "cover"
    }
```

6. Store the collected book information in a dictionary
7. Save the data into a json file as **"api_books.json"** in the **"website"** folder. This is needed for the JavaScript code to display the data.

```
with open('./website/api_books.json', 'w') as f:
    json.dump(books_dict, f, indent=4)
```
