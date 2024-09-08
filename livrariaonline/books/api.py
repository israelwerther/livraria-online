import requests

def get_want_to_read_books():
    url = "https://openlibrary.org/people/mekBot/books/want-to-read.json"
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        return None
