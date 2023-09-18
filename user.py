"""
user.py
File contains the class that represents an app's user.
"""

from Db import Db


class User:
    """Class represents a user"""

    def __init__(self, id: int = None, username: str = None, password:
                 str = None, firstname: str = None,
                 lastname: str = None) -> None:
        """
        Method for initializing the object
        """
        # User initialize
        self.id = id                # id
        self.username = username    # username
        self.password = password    # password
        self.firstname = firstname  # name
        self.lastname = lastname    # last name

        # Λίστα με τα δεδομένα του χρήστη
        self.data = [self.username, self.password, self.firstname,
                     self.lastname]

    def add_user(self) -> int:
        """Method saves a user at the data base."""

        # Connecting to database
        data_base = Db()

        # All users list
        users = data_base.select_all_users()

        # Checking if username already exists in data base
        for user in users:
            if self.username == user[1]:  # username already exists
                return False

        else:  # otherwise, user is being added in the data base
            if data_base.insert_user(self.data):    # add succeed
                return True
            else:                                   # add failed
                return False

    def delete_user(self) -> bool:
        """Method deletes a user from data base"""

        # Connecting to data base
        data_base = Db()

        if data_base.delete_user(self.data):    # delete succeed
            return True
        else:                                   # delete failed
            return False
