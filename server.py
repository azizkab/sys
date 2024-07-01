from prometheus_client import start_http_server, Counter, Gauge
import jsonpickle
import os
from typing import Final
import socketserver

count_add = Counter('count_add_book', 'Count the number of books added')
nb_books = Gauge('total_books', 'Nb of total books in library')

class MyServerTCP(socketserver.BaseRequestHandler):
    def handle(self):
        # read the characters sent by the client
        self.data = self.request.recv(1024).strip()
        action, title, author, content, book_id = self.data.decode('UTF-8').split(',')
        response = process_request(action, title, author, content, book_id)
        # return a response to the client
        self.request.sendall(bytes(response, encoding='UTF-8'))

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
            self.__content = value

    def __str__(self) -> str:
        return f"{self.__id}: {self.__title}, {self.__author}"

    def __repr__(self) -> str:
        return f"{self.__id}: {self.__title}, {self.__author}"

    def __eq__(self, other):
        return self.__id == other.__id


class MyLibrary:
    REPO_FILE: Final[str] = 'save.json'

    def __init__(self):
        self.__library = []
        self.__load()

    def add_book(self, book):
        count_add.inc()
        nb_books.inc()
        self.__library.append(book)

    def delete_book(self, id):
        nb_books.dec()
        self.__library = [book for book in self.__library if book.id != int(id)]

    def update_book(self, book):
        for book_in_lib in self.__library:
            if book.id == book_in_lib.id:
                book_in_lib.title = book.title
                book_in_lib.author = book.author
                book_in_lib.content = book.content

    def list_books(self):
        response = ''
        for book in self.__library:
            response += f'{book}\n'
        return response

    def __load(self):
        if os.path.exists(self.REPO_FILE):
            with open(self.REPO_FILE, 'r') as f:
                strjson = f.read()
                self.__library = jsonpickle.decode(strjson)._MyLibrary__library
                print(len(self.__library))
                nb_books.set(len(self.__library))

    @property
    def library(self):
        return self.__library

    def save(self):
        with open(self.REPO_FILE, 'w') as f:
            f.write(jsonpickle.encode(self))


# action,title,author,content,id
# split
def process_request(action, title = None, author = None, content = None, id = None):
    mylib = MyLibrary()
    print(f"triggered action: {action}")
    response = ''
    match action:
        case "update":
            book = Book(author=author, title=title, content=content, id=int(id))
            mylib.update_book(book)
            response = f'Book updated: {book}'
        case "new":
            book = Book(author=author, title=title, content=content)
            mylib.add_book(book)
            response = f'Book added: {book}'
        case "delete":
            mylib.delete_book(id)
            response = f'Book with id {id} deleted ...'
        case "list":
            response = mylib.list_books()
        case "list_json":
            response = jsonpickle.encode(mylib.library)
        case _:
            response = 'Unsupported action: {action}'
    mylib.save()
    return response



if __name__ == "__main__":
    start_http_server(9000)
    HOST, PORT = os.getenv('BIB_HOST', 'localhost'), int(os.getenv('BIB_PORT', 9999))
    with socketserver.TCPServer((HOST, PORT), MyServerTCP) as server:
        print(f'listening on {HOST}:{PORT}')
        server.serve_forever()