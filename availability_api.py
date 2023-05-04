import requests
import xml.etree.ElementTree as ET
import json

# Load scraped books from generated JSON file
with open("./website/api_books.json") as json_file:
    data = json.load(json_file)

result = {}

for book in data['books']:
    # Define the API endpoint and parameters
    url = "http://antwerpen.staging.aquabrowser.be/api/v1/availability/"
    params = {
        "authorization": "629e87cf5fe7767339231c6e0e1307ec",
        "frabl": book['frabl']
    }

    book_title = book['title']
    result[book_title] = {"locations": []}

    # Send the request and get the response
    response = requests.get(url, params=params)

    # Parse XML response
    root = ET.fromstring(response.content)

    # parse the XML string
    for location in root.iter('location'):
        location_name = location.get('name')
        if location_name != "Antwerpen":
            items_elem = location.find('items')
            specimen_count = 0
            location_dict = {}

            for item in items_elem.iter('item'):
                # check availability
                available = item.get('available')  #  returns "notavailable" or "loanedout": adjust in JS to display message

                # add status to library info
                status = item.find('status').text
                if status is not None:
                    location_dict['status'] = status

                # add due date to library info if status is "uitgeleend"
                if status.lower() == "uitgeleend":
                    due_date = item.find('returndate')
                    if due_date is not None:
                        location_dict['due_date'] = due_date.text

                # add count to library info
                count = item.get('count')
                specimen_count += 1

                # add place in library to library info
                sublocation = item.find('subloc')
                if sublocation is not None:
                    location_dict['sublocation'] = sublocation.text
                else:
                    location_dict['sublocation'] = None

                # add shelfmark to identify book in library
                shelfmark = item.find('shelfmark')
                if shelfmark is not None:
                    location_dict['shelfmark'] = shelfmark.text
                else:
                    location_dict['shelfmark'] = None

            location_dict['specimen_count'] = specimen_count

            # add frbl to book title
            result[book_title]['frabl'] = book['frabl']

            # add location to book title
            result[book_title]['locations'].append({location_name: location_dict})

# Save the result to a JSON file
with open('./website/availability.json', 'w') as outfile:
    json.dump(result, outfile, indent=4)
