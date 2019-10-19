import socket
from threading import Thread
import output
import encode_decode


class Acceptor_Thread(Thread):
    def __init__(self, ip, port):
        Thread.__init__(self)
        self.ip = ip
        self.port = port

    def run(self):
        try:
            data = encode_decode.recvfrom(conn)
        except ConnectionResetError:
            print("Connection closed by client")
            return
        print("Server received data:", data)
        self.connect_learner(data)
        encode_decode.sendto(conn,"SUCCESS")

    def connect_learner(self,data):
        s = socket.socket()
        ip = "127.0.0.1"
        port = 9000
        s.connect((ip, port))
        retval = encode_decode.recvfrom(s)
        encode_decode.sendto(s, data)
        retval = encode_decode.recvfrom(s)
        print(retval)



TCP_IP = '127.0.0.1'
TCP_PORT = 9500
BUFFER_SIZE = 20

tcpServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcpServer.bind((TCP_IP, TCP_PORT))
threads = []

while True:
    tcpServer.listen(5)
    print("Listening ...")
    (conn, (ip, port)) = tcpServer.accept()
    print("got connection from ",ip,port)
    conn.send(b"SUCCESS")
    newthread = Acceptor_Thread(ip, port)
    newthread.start()
    threads.append(newthread)

for t in threads:
    t.join()

