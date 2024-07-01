import jsonpickle
import os
from typing import Final

class Book:
    global_id = 0

    def __init__(self, title, author, content, id=None):
        if id == None:
            self.__id = Book.global_id
            Book.global_id = Book.global_id + 1
        else:
            self.__id = id
        self.__title = title
        self.__author = author
        self.__content = content

    @property
    def id(self):
        return self.__id

    @property
    def author(self):
        return self.__author

    @author.setter
    def author(self, value):
        if len(value) > 3:
            self.__author = value

    @property
    def title(self):
        return self.__title

    @title.setter
    def title(self, value):
        if value != None:
            self.__title = value

    @property
    def content(self):
        return self.__content

    @content.setter
    def content(self, value):
        if value != None:
            self.__content = content

    def __str__(self) -> str:
        return f"{self.__id}: {self.__title}, {self.__author}"

    def __eq__(self, other):
        return self.__id == other.__id


class MyLibrary:
    REPO_FILE: Final[str] = 'save.json'

    def __init__(self):
        self.__library = []
        self.__load()

    def add_book(self, book):
        self.__library.append(book)

    def delete_book(self, id):
        self.__library = [book for book in self.__library if book.id != id]

    def update_book(self, book):
        for book_in_lib in self.__library:
            if book.id == book_in_lib.id:
                book_in_lib.title = book.title
                book_in_lib.author = book.author
                book_in_lib.content = book.content

    def list_books(self):
        for book in self.__library:
            print(book)

    def __load(self):
        if os.path.exists(self.REPO_FILE):
            with open(self.REPO_FILE, 'r') as f:
                strjson = f.read()
                self.__library = jsonpickle.decode(strjson)._MyLibrary__library

    def save(self):
        with open(self.REPO_FILE, 'w') as f:
            f.write(jsonpickle.encode(self))



def input_book():
    title = input("title: ")
    author = input("author: ")
    content = input("content: ")
    return title, content, author


if __name__ == "__main__":
    mylib = MyLibrary()
    action = ""
    while action != "q":
        mylib.save()
        action = input("choose action: ")
        print(f"triggered action: {action}")
        match action:
            case "update":
                id = int(input("id: "))
                title, content, author = input_book()
                book = Book(author=author, title=title, content=content, id=id)
                mylib.update_book(book)
            case "new":
                title, content, author = input_book()
                book = Book(author=author, title=title, content=content)
                mylib.add_book(book)
            case "delete":
                id = int(input("id: "))
                mylib.delete_book(id)
            case "list":
                mylib.list_books()
            case _:
                pass
