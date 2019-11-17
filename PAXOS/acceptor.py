import socket
from threading import *
import output
import encode_decode
from test import *
import time
rcvd_msgs = []
lock = Lock()


def find_min():
    global proposer_fds
    global rcvd_msgs
    lock.acquire()
    a = rcvd_msgs.index(min(rcvd_msgs))
    lock.release()
    data = "PROMISE " + str(min(rcvd_msgs))
    encode_decode.sendto(proposer_fds[a], data)
    output.print_success(data)
    data = encode_decode.recvfrom(proposer_fds[a])
    output.print_success(data)
    data = data.split()
    if data[0]=="ACCEPT-REQUEST":
        data = "ACCEPT "+str(min(rcvd_msgs))
        for fd in proposer_fds:
            encode_decode.sendto(fd,data)


class Acceptor_Thread(Thread):
    def __init__(self, ip, port):
        Thread.__init__(self)
        self.ip = ip
        self.port = port

    def run(self):
        global rcvd_msgs
        try:
            data = encode_decode.recvfrom(conn)
        except ConnectionResetError:
            print("Connection closed by client")
            return
        print("Server received data:", data)
        data = data.split()
        lock.acquire()
        rcvd_msgs.append(int(data[1]))
        lock.release()


    def connect_learner(self,data):
        s = socket.socket()
        ip = "127.0.0.1"
        port = 9000
        s.connect((ip, port))
        retval = encode_decode.recvfrom(s)
        encode_decode.sendto(s, data)
        retval = encode_decode.recvfrom(s)
        print(retval)


output.print_success(":::::::::::::PAXOS ACCEPTOR:::::::::::::::")
print("Insert I.P. Address of Acceptor Node")
TCP_IP = input()
print("Insert Port number of Acceptor Node")
TCP_PORT = int(input())
insert_acceptor(TCP_IP,TCP_PORT)

tcpServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcpServer.bind((TCP_IP, TCP_PORT))
threads = []
proposer_fds = []

n = get_proposers_count()
print(n)
while True:
    for i in range(n):
        tcpServer.listen(5)
        print("Listening ...")
        (conn, (ip, port)) = tcpServer.accept()
        proposer_fds.append(conn)
        print("got connection from ",ip,port)
        conn.send(b"SUCCESS")
        newthread = Acceptor_Thread(ip, port)
        newthread.start()
        threads.append(newthread)
    time.sleep(1)
    find_min()
    proposer_fds.clear()
    rcvd_msgs.clear()
    # encode_decode.sendto(proposer_fds[0], "SUCCESS")
    # for j in range(1,n):
    #     encode_decode.sendto(proposer_fds[j], "FAILURE")
