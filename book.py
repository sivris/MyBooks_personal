"""
book.py
File contains the class Book.
"""

from Db import Db
import functions


class Book:
    """
    Class for creating objects that represents a book.

    Attributes
    ----------
    id: int
        book id
    title: str
        title of the book
    author: str
        author of the book
    publisher: str
        publisher of the book
    description: str
        description of the book
    book_cover: str
        the filepath for the image of the book cover


    Methods
    -------
    add_book(user_id)
        Adds the book in data base

    delete_book()
        Deletes the book from the data base
    """

    def __init__(self, id: int = None, title: str = None, author: str = None,
                 publisher: str = None, description: str = None,
                 book_cover=None) -> None:
        """
        Constructs all the necessary attributes for the book object.

        Parameters
        ----------
        id, title, author, publisher, description, book_cover
        """

        # constructing the attributes of the class
        self.id = id
        self.title = title                  # title
        self.author = author                # author
        self.publisher = publisher          # publisher
        self.description = description      # description
        self.book_cover = book_cover        # book cover

        # list with the attributes
        self.data = [self.title, self.author, self.publisher, self.description,
                     self.book_cover]

    def __str__(self) -> str:
        """Dunder method for printing an object book in terminal."""

        string = f"\n\"{self.title}\"\n"
        string += f"Author: {self.author}"
        string += f"\nPublished by: {self.publisher}\n"
        string += f"Description: {self.description}\n"
        string += f"Book Cover Path: {self.book_cover}\n"

        return string

    def add_book(self, user_id) -> bool:
        """
        Method adds the book in the data base.

        Parameters
        ----------
        user_id: int
            this is the id of an object User

        Returns
        -------
        bool
        """

        # connect to data base
        data_base = Db()

        # checking if book already exists in data base
        all = functions.all_books()  # list with all books

        if all:  # if any books in db
            for b in all:
                # if any book with the same title
                if b.title == self.title:
                    return False

        # adding book in db
        self.id = data_base.insert_book(self.data)

        if self.id:  # if successfully added

            # if successful addition in personal library
            if data_base.insert_user_books([user_id, self.id]):
                return True
            else:
                return False

        else:
            return False

    def delete_book(self) -> bool:
        """
        Method deletes the book from the data base.

        Returns
        -------
        bool
        """

        # connect to db
        data_base = Db()

        # delete book
        if data_base.delete_book(self.data):  # if successful delete
            return True
        else:
            return False
