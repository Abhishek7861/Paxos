import socket

class acceptor:
    def __init__(self):
        pass

    def accept_Requests(self):
        s = socket.socket()
        port = 9000
        s.bind(('', port))
        s.listen(5)
        while True:
            c, addr = s.accept()
            c.send(b'Thank you for connecting')
            c.close()

b = acceptor()
b.accept_Requests()