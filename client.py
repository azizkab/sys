import socket, os


def input_book():
    title = input("title: ")
    author = input("author: ")
    content = input("content: ")
    return title, content, author

class RemoteLib:

    def __init__(self, host = 'localhost', port = 9999):
        self.__host = host
        self.__port = port

    def __send_data(self, data):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.connect((self.__host, self.__port))
                sock.sendall(bytes(data + "\n", "utf-8"))
                received = str(sock.recv(1024), "utf-8")
                print(received)
        except ConnectionRefusedError:
            print('Connection refused: retry the action again in a moment')

    def update_book(self, author, title, content, id):
        self.__send_data(f'update,{title},{author},{content},{id}')

    def add_book(self, author, title, content):
        self.__send_data(f'new,{title},{author},{content},')

    def list_books(self):
        self.__send_data('list,,,,')

    def delete(self, id):
        self.__send_data(f'delete,,,,{id}')

if __name__ == "__main__":
    mylib = RemoteLib(
        host = os.getenv('BIB_HOST', 'localhost'),
        port = int(os.getenv('BIB_PORT', 9999))
    )
    action = ""
    while action != "q":
        action = input("choose action: ")
        print(f"triggered action: {action}")
        match action:
            case "update":
                id = int(input("id: "))
                title, content, author = input_book()
                mylib.update_book(author, title, content, id)
            case "new":
                title, content, author = input_book()
                mylib.add_book(author, title, content)
            case "delete":
                id = int(input("id: "))
                mylib.delete_book(id)
            case "list":
                mylib.list_books()
            case _:
                pass
