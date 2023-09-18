"""
book_request_creation.py
File contains:
-   Function for collecting data for a book through Google Books API.
-   Function for creating an object book.
-   Function for saving an image from web.
"""

from book import Book
from datetime import datetime
import requests
import os


def book_search(keywords: str) -> dict:
    """
    Function for collecting data for a book through Google Books API.
        args: string from the user
        returns: dictionary with book data
    """

    # book data dictionary
    book_data = {}

    # list that contains the keywords without the spaces
    list_of_keywords = keywords.split(" ")

    # joining the keywords with the character +
    merged_keywords = "+".join(list_of_keywords)

    # url that will be used
    url = f"https://www.googleapis.com/books/v1/volumes?q={merged_keywords}"

    # open url
    try:
        with requests.get(url) as response:

            # if status code 200 (ΟΚ)
            if response.status_code == 200:
                # returning the results in json
                results = response.json()

    # catch any exception
    except Exception as e:
        print(e)
        return None

    # saving the collected data in dictionary
    try:
        # saving first book's data at volume info
        volume_info = results["items"][0]["volumeInfo"]

        """Inserting data in dictionary book_data"""

        # title
        if 'title' in volume_info:
            book_data["title"] = volume_info["title"] if volume_info["title"]\
                else None
        else:
            return None

        # author
        if 'authors' in volume_info:
            book_data["authors"] = volume_info["authors"][0]\
                if volume_info["authors"][0] else None
        else:
            book_data['authors'] = 'N/A'

        # publisher
        if 'publisher' in volume_info:
            book_data["publisher"] = volume_info["publisher"]\
                if volume_info["publisher"] else None
        else:
            book_data['publisher'] = 'N/A'

        # description
        if 'description' in volume_info:
            book_data['description'] = volume_info['description']\
                if volume_info['description'] else None
        else:
            book_data['description'] = 'N/A'

        # image link
        if 'imageLinks' in volume_info:
            image_link = volume_info['imageLinks']['smallThumbnail']\
                if volume_info['imageLinks']['smallThumbnail'] else None

            # calling function for image saving
            book_cover = download_image(image_link)

            # saving image path at the dictionary
            book_data['book_cover'] = book_cover if book_cover else None

        # api did not return image
        else:
            book_data['book_cover'] = None

        return book_data

    # catch any exception
    except Exception as e:
        print(e)
        return None


def create_book(data: dict) -> Book:
    """
    Function for creating a book object.
        parameter: dictionary with book data
        returns: Book
    """
    return Book(title=data["title"], author=data["authors"],
                publisher=data["publisher"], description=data["description"],
                book_cover=data['book_cover'])


def download_image(image_link: str) -> str:
    """
    Function downloads an image and saving it in folder /covers
    Parameter: a string that has the url for the image
    """

    # defining the directory that the image will be saved
    save_directory = r"covers"

    # creating the directory if not exists
    os.makedirs(save_directory, exist_ok=True)

    # creating a string based on time for the name of the image
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')

    # joining the directory with the image name
    save_path = os.path.join(save_directory, f'image_{timestamp}.jpg')

    # open url
    response = requests.get(image_link)

    # if status code is 200 (ΟΚ)
    if response.status_code == 200:

        # open folder with Write Binary
        with open(save_path, 'wb') as file:

            # writing in the folder the contents of the url (image)
            file.write(response.content)
            return save_path

    # a fail occurred
    else:
        return False
