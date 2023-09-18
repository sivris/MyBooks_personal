"""
books_window.py
File contains a class that creates the window BOOKS.
"""

from tkinter import (Tk, Frame, Label, Listbox, messagebox, filedialog, BOTH,
                     X, Button, LEFT, Scrollbar, DISABLED, NORMAL, Toplevel,
                     END, W, Y, RIGHT)
from functions import (all_books, find_unread, user_books, find_popular,
                       remove_cover_from_db, find_popular_and_unread,
                       process_image, add_to_my_library, save_image_in_db)
from user import User


class BooksWindow:
    """
    Function creates a window in which the user can explore all the books in
    the app.
    """
    def __init__(self, user: User) -> None:
        """
        In the __init__ method I create the window and the necessary attributes
        for the object.
        """

        # attribute user is a User object and represents the connected user in
        # the app
        self.user = user

        """
        Connecting to data base and creating the attributes for the list
        books.
        """

        # list with all books
        self.books = all_books()

        # list with read books
        self.user_books = user_books(self.user.id)

        # attribute for the selected book cover
        self.image = None

        # attribute for the selected book
        self.selected_book = None

        # create window
        self.root = Tk()
        self.root.title('MyBooks')

        # define the icon
        try:
            self.root.iconbitmap(r"covers\app_icon.ico")
        except Exception as e:
            print(e)

        # optimize the window
        self.root.config(background='light green')
        self.root.geometry('1200x650')

        # upper frame
        self.upper_frame = Frame(master=self.root, background='light green',
                                 relief='groove', borderwidth=2)
        self.upper_frame.pack(fill=BOTH)

        # frame for buttons (all, popular, unread)
        self.frame_buttons = Frame(master=self.upper_frame,
                                   background='light green')
        self.frame_buttons.pack(fill=X)

        # buttons creation
        self.button1 = Button(master=self.frame_buttons,
                              background='light yellow', text='All Books',
                              font=('consolas', 10, 'bold'),
                              command=self.show_all_books, width=25)

        self.button2 = Button(master=self.frame_buttons,
                              background='light yellow', text='Popular Books',
                              font=('consolas', 10, 'bold'),
                              command=self.popular_books, width=25)

        self.button3 = Button(master=self.frame_buttons,
                              background='light yellow', text='Unread Books',
                              font=('consolas', 10, 'bold'),
                              command=self.unread_books, width=25)

        self.button4 = Button(master=self.frame_buttons,
                              background='light yellow',
                              text='Popular & Unread Books',
                              font=('consolas', 10, 'bold'),
                              command=self.popular_and_unread, width=25)

        self.button1.grid(row=0, column=0, padx=10, pady=2)
        self.button2.grid(row=0, column=1, padx=10, pady=2)
        self.button3.grid(row=0, column=2, padx=10, pady=2)
        self.button4.grid(row=0, column=3, padx=10, pady=2)

        # frame for message for the selected button
        self.message_frame = Frame(master=self.upper_frame,
                                   background='light green')
        self.message_frame.pack(fill=BOTH, pady=5)

        # label for the message
        self.message = Label(master=self.message_frame,
                             background='light salmon', text='',
                             font=('consolas', 11, 'bold'),
                             highlightthickness=1, highlightbackground='black')
        self.message.pack()

        #  frame for listbox
        self.listbox_frame = Frame(self.root)
        self.listbox_frame.pack(side=LEFT, fill=BOTH)

        #  scrollbar for listbox
        self.scrollbar = Scrollbar(self.listbox_frame)
        self.scrollbar.pack(side=RIGHT, fill=Y)

        #  listbox
        self.listbox = Listbox(self.listbox_frame,
                               font=('consolas', 10, 'bold'),
                               yscrollcommand=self.scrollbar.set,
                               borderwidth=4, relief='groove',
                               background='light blue')

        # connect scrollbar with listbox
        self.scrollbar.config(command=self.listbox.yview)

        # section for book info
        self.details_frame = Frame(master=self.root, background='light green')
        self.details_frame.pack(side=RIGHT, fill=BOTH, expand=True)

        '''Labels for the section Book Info'''

        # Title
        self.book_title = Label(self.details_frame, background='light green',
                                text="Title: ", font=('consolas'), anchor=W)
        self.book_title.pack()

        # Author
        self.book_author = Label(self.details_frame, background='light green',
                                 text="Author: ", font=('consolas'), anchor=W)
        self.book_author.pack()

        # Publisher
        self.book_publisher = Label(self.details_frame,
                                    background='light green',
                                    text="Publisher: ", font=('consolas'),
                                    anchor=W)
        self.book_publisher.pack()

        # Description
        self.book_description = Label(self.details_frame,
                                      background='light green',
                                      text="Description: ", font=('consolas'),
                                      wraplength=650, anchor=W)
        self.book_description.pack()

        # Image
        self.book_cover = Label(self.details_frame, background='light green')
        self.book_cover.pack()

        # Frame for buttons
        self.details_button_frame = Frame(master=self.details_frame,
                                          background='light green')
        self.details_button_frame.pack()

        # button add or change cover
        self.select_image_button = Button(master=self.details_button_frame,
                                          background='yellow',
                                          activebackground='blue',
                                          text='ADD COVER',
                                          font=('consolas', 10, 'bold'),
                                          state=DISABLED)
        self.select_image_button.grid(row=0, column=0, padx=10, pady=5)

        # button remove cover
        self.remove_cover_button = Button(self.details_button_frame,
                                          background='red', foreground='white',
                                          activebackground='white',
                                          text='REMOVE COVER',
                                          font=('consolas', 10, 'bold'),
                                          state=DISABLED)
        self.remove_cover_button.grid(row=0, column=1, padx=10, pady=5)

        # button add to my library
        self.add_button = Button(master=self.details_button_frame,
                                 background='light blue', foreground='blue',
                                 activebackground='blue',
                                 text='ADD TO MY LIBRARY',
                                 font=('consolas', 10, 'bold'), state=DISABLED)
        self.add_button.grid(row=1, column=0, padx=10, pady=5, columnspan=2)

        # starting the window
        self.show_all_books()  # calling the function for the button all books
        self.root.mainloop()

        return None

    def show_all_books(self) -> None:
        """
        Method for the button all books. It shows all books in the list box.
        """

        # define the selected book to None so the previous info to disappear
        self.selected_book = None

        # clearing the details section
        self.clear_details()

        # disabling button All books
        self.button1.config(state=DISABLED)
        self.button2.config(state=NORMAL)
        self.button3.config(state=NORMAL)
        self.button4.config(state=NORMAL)

        # display the message
        self.message.config(text='ALL BOOKS')

        # deleting old books from the listbox
        self.listbox.delete(0, END)

        # finding the max width of all the titles that will be inserted in the
        # listbox to configure the listbox width
        max_width = 0
        for item in self.books:
            if len(item.title) > max_width:
                max_width = len(item.title)

        # inserting the new books in the listbox
        for i, book in enumerate(self.books):
            self.listbox.insert(END, f'{i+1}) {book.title}')

        # configuring the listbox width
        self.listbox.config(width=max_width+5)

        # pack listbox
        self.listbox.pack(side=LEFT, fill=BOTH, expand=True)

        # binding the event selection from listbox with the
        # function show_book_info
        self.listbox.bind("<<ListboxSelect>>", self.show_book_info)

        return None

    def popular_books(self) -> None:
        """
        Method displays the 10 most popular books in the app based on how many
        users read the book.
        """

        # define the selected book to None so the previous info to disappear
        self.selected_book = None

        # clearing the details section
        self.clear_details()

        # getting books sorted by popularity
        self.popular_books_list = find_popular()

        # keeping the 10 most popular books
        self.popular_books_list = self.popular_books_list[:10]

        # display the message
        self.message.config(text='THE 10 MOST POPULAR BOOKS IN THE APP')

        # disabling button Popular books
        self.button1.config(state=NORMAL)
        self.button2.config(state=DISABLED)
        self.button3.config(state=NORMAL)
        self.button4.config(state=NORMAL)

        # deleting old books from the listbox
        self.listbox.delete(0, END)

        # finding the max width of all the titles that will be inserted in the
        # listbox to configure the listbox width
        max_length = 0
        for item in self.popular_books_list:
            if len(item.title) > max_length:
                max_length = len(item.title)

        # inserting the new books in the listbox
        for i, book in enumerate(self.popular_books_list):
            self.listbox.insert(END, f'{i+1}) {book.title}')

        # configuring the listbox width
        self.listbox.config(width=max_length+5)

        # pack listbox
        self.listbox.pack(side=LEFT, fill=BOTH, expand=True)

        # binding the event selection from listbox with the
        # function show_book_info
        self.listbox.bind("<<ListboxSelect>>", self.show_book_info)

        return None

    def unread_books(self) -> None:
        """
        Method displays the unread books for the current user in the listbox.
        """

        # define the selected book to None so the previous info to disappear
        self.selected_book = None

        # clear details section
        self.clear_details()

        # getting the unread books
        self.unread_books_list = find_unread(self.user.id)

        # deleting old books from the listbox
        self.listbox.delete(0, END)

        # disabling button Unread books
        self.button1.config(state=NORMAL)
        self.button2.config(state=NORMAL)
        self.button3.config(state=DISABLED)
        self.button4.config(state=NORMAL)

        # display message
        self.message.config(text='THE BOOKS YOU HAVE NOT READ')

        # if there are no unread books, function terminates
        if not self.unread_books_list:
            return None

        # finding the max width of all the titles that will be inserted in the
        # listbox to configure the listbox width
        max_length = 0
        for item in self.unread_books_list:
            if len(item.title) > max_length:
                max_length = len(item.title)

        # inserting the new books in the listbox
        for i, book in enumerate(self.unread_books_list):
            self.listbox.insert(END, f'{i+1}) {book.title}')

        # configuring the listbox width
        self.listbox.config(width=max_length+5)

        # pack listbox
        self.listbox.pack(side=LEFT, fill=BOTH, expand=True)

        # binding the event selection from listbox with the
        # function show_book_info
        self.listbox.bind("<<ListboxSelect>>", self.show_book_info)

        return None

    def popular_and_unread(self) -> None:
        """
        Method displays the popular and unread books for the current user
        """

        # define the selected book to None so the previous info to disappear
        self.selected_book = None

        # clear details section
        self.clear_details()

        # getting the list with the books
        self.popular_and_unread_list = find_popular_and_unread(self.user.id)

        # deleting old books from the listbox
        self.listbox.delete(0, END)

        # disabling the button Popular & Unread books
        self.button1.config(state=NORMAL)
        self.button2.config(state=NORMAL)
        self.button3.config(state=NORMAL)
        self.button4.config(state=DISABLED)

        # display message
        self.message.config(text='POPULAR BOOKS YOU HAVE NOT READ')

        # if there are no books in the list function terminates
        if not self.popular_and_unread_list:
            return None

        # finding the max width of all the titles that will be inserted in the
        # listbox to configure the listbox width
        max_length = 0
        for item in self.popular_and_unread_list:
            if len(item.title) > max_length:
                max_length = len(item.title)

        # inserting the new books in the listbox
        for i, book in enumerate(self.popular_and_unread_list):
            self.listbox.insert(END, f'{i+1}) {book.title}')

        # configuring the listbox width
        self.listbox.config(width=max_length+5)

        # pack listbox
        self.listbox.pack(side=LEFT, fill=BOTH, expand=True)

        # binding the event selection from listbox with the
        # function show_book_info
        self.listbox.bind("<<ListboxSelect>>", self.show_book_info)

        return None

    def show_book_info(self, event) -> None:
        """
        Method takes the selection index and displays the book info in the
        right section of the window.
        """

        # internal method
        def add():
            """
            Function is used from the button ADD TO MY LIBRARY.
            Then, the function calls the method self.add_global with the
            necessary parameters.
            """
            self.add_global(self.user, self.selected_book)

        # getting the index from the selection of the listbox
        # selection looks like this (1,)
        selection = event.widget.curselection()

        if selection:
            # getting the number form the index without the comma
            index = selection[0]

            # saving the string from the selection data
            data = event.widget.get(index)

            # find the parenthesis after the number (data looks like: 1) 1984
            title_index = data.find(')')

            # keeping only the title of the book
            title = data[title_index+1:].strip()

            # finding the book from the list of all books
            for book in self.books:
                if title == book.title:
                    self.selected_book = book
                    break

            # Configuring the labels for displaying the details of the book
            self.book_title.config(
                text=f"Title:\n{self.selected_book.title}\n",
                font=('consolas', 12))

            self.book_author.config(
                text=f"Author:\n{self.selected_book.author}\n")

            self.book_publisher.config(
                text=f"Publisher:\n{self.selected_book.publisher}\n")

            # decreasing the length of the description of necessary
            if len(self.selected_book.description) > 450:
                short_descr = self.selected_book.description[:450] + '...'
                # Εμφάνιση του μειωμένου description
                self.book_description.config(
                    text=f'Description:\n{short_descr}\n')

                # binding the cursor events in the description label for
                # displaying the full description
                self.book_description.bind('<Enter>', self.show_more)
                self.book_description.bind('<Leave>', self.destroy_sub_root)

            else:  # there is no need for decrease
                # inserting the full description
                self.book_description.config(
                    text=f'Description:\n{self.selected_book.description}\n')

                # unbinding the cursor events
                self.book_description.unbind('<Enter>')
                self.book_description.unbind('<Leave>')

            # fixing the image
            self.fix_the_image()

            # activating the buttons
            self.details_button_frame.pack(pady=15)
            self.add_button.config(command=add, state=NORMAL)
            self.select_image_button.config(command=self.add_change_cover,
                                            state=NORMAL)

            # activating the remove cover button if there is a book cover
            if self.selected_book.book_cover:
                self.remove_cover_button.config(command=self.remove_cover,
                                                state=NORMAL)

            # else the button is disabled
            else:
                self.remove_cover_button.config(state=DISABLED)

            return None

    def fix_the_image(self) -> None:
        """
        Method calls the function process image. The returned object is a
        PhotoImage. Finally, the method fixes the image inside the window.
        """
        if self.selected_book.book_cover:  # if filepath
            # saving the PhotoImage in an attribute
            self.image = process_image(filepath=self.selected_book.book_cover,
                                       master=self.details_frame)

            if not self.image:  # function returned false
                # disappearing the image label
                self.book_cover.forget()

                # changing the button name
                self.select_image_button.config(text='ADD COVER')
                # disabling the button remove cover
                self.remove_cover_button.config(state=DISABLED)

                # function terminates
                return None

            # configuring the image label to display the image
            self.book_cover.config(image=self.image, highlightthickness=2,
                                   highlightbackground='black')
            self.book_cover.pack()

            # button name to "CHANGE IMAGE"
            self.select_image_button.config(text='CHANGE COVER')

            # rearrange the buttons
            self.details_button_frame.forget()
            self.details_button_frame.pack()

        else:  # if not filepath
            # disappearing the image label
            self.book_cover.forget()

            # changing the button name
            self.select_image_button.config(text='ADD COVER')

        return None

    def add_global(self, user, book) -> None:
        """
        Method is called from button add to my library to add the selected book
        in user's library.
        """

        # call the function for adding a book and save the returned value in a
        # variable
        returned_value = add_to_my_library(user.id, book.id)

        # checking the returned value
        if returned_value is False:
            messagebox.showerror('ERROR',
                                 'This book is already in your library.')
            return None
        elif returned_value:
            messagebox.showinfo('SUCCESS', 'Book added to your library.')
        else:
            messagebox.showerror('ERROR',
                                 'Something went wrong. Try again later.')

        return None

    def show_more(self, event) -> None:
        """
        Method is used to display a TopLevel window that displays the full
        description of a book when this is necessary.
        """

        # creating window
        self.sub_root = Toplevel(self.root)

        # hide the decorations of the window
        self.sub_root.wm_overrideredirect(True)

        # define the geometry of the window and its position
        self.sub_root.wm_geometry(f"+{event.x_root+10}+{event.y_root+10}")

        # Εισαγωγή του label με τη πλήρη περιγραφή του βιβλίου
        self.sub_root_label = Label(self.sub_root,
                                    text=self.selected_book.description,
                                    wraplength=500, background='light blue')
        self.sub_root_label.pack()

        return None

    def destroy_sub_root(self, event) -> None:
        """
        Method destroys the TopLevel window for the full description
        """
        self.sub_root.destroy()

        return None

    def add_change_cover(self) -> None:
        """
        Method gives functionality to button Add/Change Cover.
        """

        # getting the filepath by opening the windows explorer
        filepath = filedialog.askopenfilename(filetypes=[("Image Files",
                                                          "*.png;*.jpg;*.jpeg;"
                                                          )])

        # if user close the filedialog window
        if not filepath:
            return None

        # saving the filepath in data base
        if save_image_in_db(filepath, self.selected_book):  # if succeed

            # updating the list with all books
            self.books = all_books()

            # iterating all books to find again the already selected book but
            # now the image will be displayed
            if self.books:
                for book in self.books:

                    if book.id == self.selected_book.id:  # if found
                        # update the selected book
                        self.selected_book = book
                        break

                # fix the image in the window
                self.fix_the_image()

        else:  # image update did not succeed
            messagebox.showerror('ERROR',
                                 'Failed to add/change cover. Try again later.'
                                 )

    def remove_cover(self) -> None:
        """
        Method used for removing a cover from a book.
        """

        # asking user if really wants to delete the cover
        if messagebox.askyesno('REMOVE COVER',
                               'Do you want to remove the book cover?'):

            # calling function for removing the cover
            if remove_cover_from_db(book=self.selected_book):

                # updating the list with all books
                self.books = all_books()

                # iterating all books to find again the already selected book
                # but now the image will be not be displayed
                if self.books:
                    for book in self.books:

                        if book.id == self.selected_book.id:  # if found
                            # updating the selected book
                            self.selected_book = book
                            break

                    # fixing the image in the window
                    self.fix_the_image()

                    # disabling the button remove cover
                    self.remove_cover_button.config(state=DISABLED)
                    return None

            else:  # cover removal did not succeed
                messagebox.showerror('ERROR',
                                     'Failed to remove cover. Try again later.'
                                     )
                return None

        else:  # user answered no
            return None

    def clear_details(self) -> None:
        """
        Method for clearing the details section when there is no book selected
        """

        # disabling the buttons
        self.add_button.config(state=DISABLED)
        self.select_image_button.config(state=DISABLED)
        self.remove_cover_button.config(state=DISABLED)

        # clearing the labels
        self.book_author.config(text='')
        self.book_publisher.config(text='')
        self.book_description.config(text='')
        self.book_cover.forget()
        self.details_button_frame.forget()

        # display a message
        self.book_title.config(text='CHOOSE A BOOK FROM THE LIST',
                               font=('consolas', 20, 'bold'))

        return None
