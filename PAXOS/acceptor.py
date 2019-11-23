import socket
from threading import *
import output
import encode_decode
from test import *
import time
rcvd_msgs = []
lock = Lock()
nlock = Lock()
n = 0


def find_min():
    global proposer_fds
    global rcvd_msgs
    global lock
    if len(rcvd_msgs) == 0:
        return
    lock.acquire()
    a = rcvd_msgs.index(min(rcvd_msgs))
    lock.release()
    data = "PROMISE " + str(max(rcvd_msgs))
    encode_decode.sendto(proposer_fds[a], data)
    output.print_success(data)
    data = encode_decode.recvfrom(proposer_fds[a])
    output.print_success(data)
    data = data.split()
    if data[0]=="ACCEPT-REQUEST":
        data = "ACCEPT "+str(min(rcvd_msgs))+" "+data[2]+" "+data[3]
        for fd in proposer_fds:
            encode_decode.sendto(fd,data)
        result = get_learners()
        ipport = []
        learner_socket = []
        for i in result:
            s = socket.socket()
            ipport.append(i)
            learner_socket.append(s)
        for fd in learner_socket:
            i = ipport.pop()
            try:
                fd.connect((i[0],i[1]))
            except ConnectionRefusedError:
                output.print_failure("Learner not running")
                return
            retval = encode_decode.recvfrom(fd)
            output.print_running(retval)
        for fd in learner_socket:
            encode_decode.sendto(fd, data)
        for fd in learner_socket:
            retval = encode_decode.recvfrom(fd)
            output.print_running(retval)

class update_n(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
            global n
            global nlock
            while (1):
                nlock.acquire()
                n = get_proposers_count()
                # print(n)
                nlock.release()
                time.sleep(1)


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
        if data[0]=="EXIT":
            return
        lock.acquire()
        rcvd_msgs.append(float(data[1]))
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


output.print_running(":::::::::::::PAXOS ACCEPTOR:::::::::::::::")
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
newthread = update_n()
newthread.start()
threads.append(newthread)

count=0
while True:
        tcpServer.listen(5)
        output.print_running("Listening ...")
        count = count+1
        (conn, (ip, port)) = tcpServer.accept()
        proposer_fds.append(conn)
        print("got connection from ",ip,port)
        conn.send(b"SUCCESS")
        newthread = Acceptor_Thread(ip, port)
        newthread.start()
        threads.append(newthread)
        if count ==n:
            time.sleep(1)
            find_min()
            count=0
            proposer_fds.clear()
            rcvd_msgs.clear()
    # encode_decode.sendto(proposer_fds[0], "SUCCESS")
    # for j in range(1,n):
    #     encode_decode.sendto(proposer_fds[j], "FAILURE")
