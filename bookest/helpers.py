import requests
import json
import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
NYT_URL = os.getenv("NYT_URL")
NYT_API_KEY = os.getenv("NYT_API_KEY")
OAUTH_GOOGLE = os.getenv("OAUTH_GOOGLE")


def get_book_credentials(data): 
    google_id = data["googleId"]
    isbn = data["isbn"]
    title = data["title"]
    no_cover = data["noCover"]
    will_be_read = data["willBeRead"]
    has_been_read = data["hasBeenRead"]
    shelf = "will_be_read" if will_be_read else "has_been_read"
    other_shelf = "will_be_read" if has_been_read else "has_been_read"
    return {
        "book_data":
        {
            "google_id": google_id,
            "isbn": isbn,
            "title": title,
            "no_cover": no_cover,
        },
        "shelf_data":
        {
            "shelf": shelf,
            "other_shelf": other_shelf
        }
    }


def get_review_credentials(data):
    google_id = data["googleId"]
    isbn = data["isbn"]
    title = data["title"]
    no_cover = data["noCover"]
    content = data["content"]
    _id = data["_id"]
    return {
        "book_data":
        {
            "google_id": google_id,
            "isbn": isbn,
            "title": title,
            "no_cover": no_cover,
        },
        "content_data":
        {
            "content": content,
            "_id": _id
        }
    }


def get_book_on_notes(data):
    google_id = data["googleId"]
    isbn = data["isbn"]
    title = data["title"]
    no_cover = data["noCover"]
    return {
        "google_id": google_id,
        "isbn": isbn,
        "title": title,
        "no_cover": no_cover,
    }


def get_user(token):
    response = requests.get(f"{OAUTH_GOOGLE}{token}")
    if response.status_code == 200:
        user_data = json.loads(response.content)
        return user_data
    else:
        return None


def get_books_genre(genre):
    url = f"{NYT_URL}/{genre}.json?api-key={NYT_API_KEY}"
    books = requests.get(url).json()
    return books
