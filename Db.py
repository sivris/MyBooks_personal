"""
Db.py
This file contains the class Db that has methods for interacting with the data
base.
"""
import sqlite3


class Db:
    """
    Class for interacting with the data base books.db.
    """
    def __init__(self) -> None:
        """Establishing the connection with the data base."""
        self.conn = sqlite3.connect("books.db")

    def insert_user(self, data) -> int:
        """Method for inserting values in table users."""
        try:
            cursor = self.conn.cursor()  # creating the cursor
            sql = "INSERT INTO users (username, password, firstname, lastname)\
                   VALUES (?, ?, ?, ?)"
            cursor.execute(sql, data)
            self.conn.commit()  # commit any changes
            return cursor.lastrowid
        # catching any exceptions
        except Exception as e:
            print(e)
            return 0

    def insert_book(self, data) -> int:
        """Method for inserting values in table books."""
        try:
            cursor = self.conn.cursor()  # creating the cursor
            sql = "INSERT INTO books (title, author, publisher, description,\
                book_cover) VALUES (?, ?, ?, ?, ?)"
            cursor.execute(sql, data)
            self.conn.commit()  # commit any changes
            return cursor.lastrowid
        # catching any exceptions
        except Exception as e:
            print(e)
            return 0

    def insert_rating(self, data) -> int:
        """Method for inserting values in table ratings."""
        try:
            cursor = self.conn.cursor()  # creating the cursor
            sql = "INSERT INTO ratings (user_id, book_id, comment, rating)\
                VALUES (?, ?, ?, ?)"
            cursor.execute(sql, data)
            self.conn.commit()  # commit any changes
            return cursor.lastrowid
        # catching any exceptions
        except Exception as e:
            print(e)
            return 0

    def insert_user_books(self, data) -> int:
        """Method for inserting values in table user_books"""
        try:
            cursor = self.conn.cursor()  # creating the cursor
            sql = 'INSERT INTO user_books (user_id, book_id) VALUES (?, ?)'
            cursor.execute(sql, data)
            self.conn.commit()  # commit any changes
            return cursor.lastrowid
        # catching any exceptions
        except Exception as e:
            print(e)
            return 0

    def delete_user(self, id) -> bool:
        """Method for deleting rows from table users"""
        try:
            cursor = self.conn.cursor()  # creating the cursor
            sql = "DELETE FROM users WHERE id = ?"
            cursor.execute(sql, (id,))
            self.conn.commit()  # commit any changes
            return 1
        # catching any exceptions
        except Exception as e:
            print(e)
            return 0

    def delete_book(self, id) -> bool:
        """Method for deleting rows from table books"""
        try:
            cursor = self.conn.cursor()  # creating the cursor
            sql = "DELETE FROM books WHERE id = ?"
            cursor.execute(sql, (id,))
            self.conn.commit()
            return 1
        # catching any exceptions
        except Exception as e:
            print(e)
            return 0

    def delete_rating(self, id) -> bool:
        """Method for deleting rows from table ratings"""
        try:
            cursor = self.conn.cursor()  # creating the cursor
            sql = "DELETE FROM ratings WHERE id = ?"
            cursor.execute(sql, (id,))
            self.conn.commit()  # commit any changes
            return 1
        # catching any exceptions
        except Exception as e:
            print(e)
            return 0

    def delete_user_books(self, id) -> bool:
        """Method for deleting rows from table user_books"""
        try:
            cursor = self.conn.cursor()  # creating the cursor
            sql = 'DELETE FROM user_books WHERE book_id = ?'
            cursor.execute(sql, (id,))
            self.conn.commit()  # commit any changes
            return 1
        # catching any exceptions
        except Exception as e:
            print(e)
            return 0

    def update_user(self, data) -> bool:
        """Method for updating the values in a row in the table users."""
        try:
            cursor = self.conn.cursor()  # creating the cursor
            sql = "UPDATE users SET username = ?, password = ?, firstname = ?,\
                lastname = ? WHERE id = ?"
            cursor.execute(sql, data)
            self.conn.commit()  # commit any changes
            return 1
        # catching any exceptions
        except Exception as e:
            print(e)
            return 0

    def update_book(self, data) -> bool:
        """Method for updating the values in a row in the table books."""
        try:
            cursor = self.conn.cursor()  # creating the cursor
            sql = "UPDATE books SET title = ?, author = ?, publisher = ?,\
                description = ? WHERE id = ?"
            cursor.execute(sql, data)
            self.conn.commit()  # commit any changes
            return 1
        # catching any exceptions
        except Exception as e:
            print(e)
            return 0

    def update_book_image(self, data) -> bool:
        """Method for updating the column filepath in a row of table books."""
        try:
            cursor = self.conn.cursor()  # creating the cursor
            sql = "UPDATE books SET book_cover = ? WHERE id = ?"
            cursor.execute(sql, data)
            self.conn.commit()  # commit any changes
            return 1
        # catching any exceptions
        except Exception as e:
            print(e)
            return 0

    def update_rating(self, data) -> bool:
        """Method for updating a row in table ratings."""
        try:
            cursor = self.conn.cursor()  # creating the cursor
            sql = "UPDATE ratings SET user_id = ?, book_id = ?, comment = ?,\
            rating = ? WHERE id = ?"
            cursor.execute(sql, data)
            self.conn.commit()  # commit any changes
            return 1
        # catching any exceptions
        except Exception as e:
            print(e)
            return 0

    def select_user_by_id(self, id) -> list:
        """Method for searching in table users using the id."""
        try:
            cursor = self.conn.cursor()  # creating the cursor
            sql = "SELECT * FROM users WHERE id = ?"
            cursor.execute(sql, (id,))
            return cursor.fetchall()
        # catching any exceptions
        except Exception as e:
            print(e)
            return 0

    def select_book_by_id(self, id) -> list:
        """Method for searching in table books using the id."""
        try:
            cursor = self.conn.cursor()  # creating the cursor
            sql = "SELECT * FROM books WHERE id = ?"
            cursor.execute(sql, (id,))
            return cursor.fetchall()
        # catching any exceptions
        except Exception as e:
            print(e)
            return 0

    def select_rating(self, user_id, book_id) -> list:
        """
        Method for searching in table ratings using a user id and a book id.
        """
        try:
            cursor = self.conn.cursor()  # creating the cursor
            sql = "SELECT comment, rating FROM ratings WHERE book_id = ? AND\
                user_id = ?"
            cursor.execute(sql, (book_id, user_id))
            return cursor.fetchall()
        # catching any exceptions
        except Exception as e:
            print(e)
            return 0

    def select_user_by_username(self, username) -> list:
        """Method for searching in table users using the username."""
        try:
            cursor = self.conn.cursor()  # creating the cursor
            sql = "SELECT * FROM users WHERE username = ?"
            cursor.execute(sql, (username,))
            return cursor.fetchall()
        # catching any exceptions
        except Exception as e:
            print(e)
            return 0

    def select_book_by_title(self, title) -> list:
        """Method for searching in books using the title."""
        try:
            cursor = self.conn.cursor()  # creating the cursor
            sql = "SELECT * FROM books WHERE title LIKE ?"
            # character % is used for returning any results that has in them
            # the string title
            cursor.execute(sql, ('%'+title+'%',))
            return cursor.fetchall()
        # catching any exceptions
        except Exception as e:
            print(e)
            return 0

    def select_book_by_author(self, author) -> list:
        """Method for searching in books using the author."""
        try:
            cursor = self.conn.cursor()  # creating the cursor
            sql = "SELECT * FROM books WHERE author LIKE ?"
            # character % is used for returning any results that has in them
            # the string title
            cursor.execute(sql, ('%'+author+'%',))
            return cursor.fetchall()
        # catching any exceptions
        except Exception as e:
            print(e)
            return 0

    def select_book_by_publisher(self, publisher) -> list:
        """Method for searching in books using the publisher."""
        try:
            cursor = self.conn.cursor()  # creating the cursor
            sql = "SELECT * FROM books WHERE publisher = ?"
            cursor.execute(sql, (publisher,))
            return cursor.fetchall()
        # catching any exceptions
        except Exception as e:
            print(e)
            return 0

    def select_all_users(self) -> list:
        """Method for returning all the data from table users"""
        try:
            cursor = self.conn.cursor()  # creating the cursor
            sql = "SELECT * FROM users ORDER BY username asc"
            cursor.execute(sql)
            return cursor.fetchall()
        # catching any exceptions
        except Exception as e:
            print(e)
            return 0

    def select_all_books(self) -> list:
        """Method for returning all the data from table books"""
        try:
            cursor = self.conn.cursor()  # creating the cursor
            sql = "SELECT * FROM books ORDER BY title asc"
            cursor.execute(sql)
            return cursor.fetchall()
        # catching any exceptions
        except Exception as e:
            print(e)
            return 0

    def select_all_ratings(self) -> list:
        """Method for returning all the data from table ratings"""
        try:
            cursor = self.conn.cursor()  # creating the cursor
            sql = 'SELECT * FROM ratings ORDER BY id'
            cursor.execute(sql)
            return cursor.fetchall()
        # catching any exceptions
        except Exception as e:
            print(e)
            return 0

    def select_all_user_books(self) -> list:
        """Method for returning all the data from table users"""
        try:
            cursor = self.conn.cursor()  # creating the cursor
            sql = 'SELECT * FROM user_books'
            cursor.execute(sql)
            return cursor.fetchall()
        # catching any exceptions
        except Exception as e:
            print(e)
            return 0
