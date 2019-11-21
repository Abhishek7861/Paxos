import socket
from threading import Thread
import output
import encode_decode
from test import *

data_store = {
    "key":"value"
}

class Learner_Thread(Thread):
    def __init__(self, ip, port):
        Thread.__init__(self)
        self.ip = ip
        self.port = port

    def run(self):
        try:
            proposer_socket=[]
            ipport = []
            global base
            global conn
            # valuepair = data
            # base = time.time()
            # data = "PREPARE "+str(base)
            result = get_proposers()
            for i in result:
                s = socket.socket()
                ipport.append(i)
                proposer_socket.append(s)
            for fd in proposer_socket:
                i = ipport.pop()
                fd.connect((i[0],i[1]))
                retval = encode_decode.recvfrom(fd)
                output.print_running(retval)
            # data = encode_decode.recvfrom(conn)
            data=retval
        except ConnectionResetError:
            print("Connection closed")
            return
        print(data)
        decoded_data = data.split()
        if decoded_data[0]=="SEARCH":
            if data_store.get(decoded_data[1]):
                value = data_store[decoded_data[1]]
                string = "FOUND!! key:"+decoded_data[1]+" value:"+value
                encode_decode.sendto(conn, string)
            else:
                string = "NOT FOUND!!"
                encode_decode.sendto(conn, string)
        if decoded_data[0] =="STORE":
            print("Stored")
            string = "SUCCESS!!"
            encode_decode.sendto(conn, string)

    def connect_acceptor(self):
        pass


TCP_IP = '127.0.0.1'
TCP_PORT = 9000
BUFFER_SIZE = 20
insert_learner(TCP_IP,TCP_PORT)

tcpServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcpServer.bind((TCP_IP, TCP_PORT))
threads = []

while True:
    tcpServer.listen(5)
    print("Listening ...")
    (conn, (ip, port)) = tcpServer.accept()
    print("got connection from ", ip, port)
    conn.send(b"SUCCESS")
    newthread = Learner_Thread(ip, port)
    newthread.start()
    threads.append(newthread)


