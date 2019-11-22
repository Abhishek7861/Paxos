import socket
from threading import *
import output
import encode_decode
import configparser
from test import *
import random
import time
import signal
import sys
import time



base=0
flag=True
TCP_PORT = 0
class temp(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        global TCP_PORT

        output.print_running(":::::::::::::PAXOS PROPOSER:::::::::::::::")
        print("Insert I.P. Address of Proposer Node")
        TCP_IP = input()
        print("Insert Port number of Proposer Node")
        TCP_PORT = int(input())

        insert_proposer(TCP_IP, TCP_PORT)
        tcpServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcpServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        tcpServer.bind((TCP_IP, TCP_PORT))
        threads = []
        client_fd = []
        a = 0
        while True:
            tcpServer.listen(5)
            output.print_running("Listening ...")
            (conn, (ip, port)) = tcpServer.accept()
            output.print_success("got connected from " + str(ip) + ":" + str(port))
            conn.send(b"SUCCESS")
            client_fd.append(conn)
            newthread = Proposer_Thread(ip, port, client_fd[a])
            a = a + 1
            newthread.start()
            threads.append(newthread)


class Proposer_Thread(Thread):
    def __init__(self, ip, port,conn):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.conn = conn

    def run(self):
            print("qdwqe")
            try:
                data = encode_decode.recvfrom(self.conn)
            except ConnectionResetError:
                print("Connection closed by client")
                return
            output.print_primary("Server received data: "+ data)
            self.connect_acceptor(data.split())


    def connect_acceptor(self,data):
        acceptor_socket=[]
        ipport = []
        global base
        global flag
        valuepair = data
        base = time.time()
        data = "PREPARE "+str(base)
        result = get_acceptors()
        acceptor_socket2 = []
        for i in result:
            s = socket.socket()
            ipport.append(i)
            acceptor_socket.append(s)
        for j in range(len(acceptor_socket)):
            i = ipport.pop()
            try:
                acceptor_socket[j].connect((i[0],i[1]))
                print(i)
                acceptor_socket2.append(acceptor_socket[j])
            except ConnectionRefusedError:
                output.print_failure("Acceptor not running: "+str(i[0])+":"+str(i[1]))
                continue
            retval = encode_decode.recvfrom(acceptor_socket[j])
        # print(len(acceptor_socket2))
        if len(acceptor_socket2)==0:
            encode_decode.sendto(self.conn,"No acceptor running")
            output.print_failure("No acceptor running")
            return
        for fd in acceptor_socket2:
            encode_decode.sendto(fd,data)
        for fd in acceptor_socket2:
            retval = encode_decode.recvfrom(fd)
            output.print_running(retval)
            retval = retval.split()
        if retval[0]=='PROMISE':
            output.print_success(retval)
            data = "ACCEPT-REQUEST "+str(base)+" "+valuepair[1]+" "+valuepair[2]
            for fd in acceptor_socket2:
                encode_decode.sendto(fd, data)
            for fd in acceptor_socket2:
                retval = encode_decode.recvfrom(fd)
                print(retval)
            print("sent success to client")
            encode_decode.sendto(self.conn, "SUCCESS")
        elif retval[0]=='ACCEPT':
            base = float(retval[1])
            encode_decode.sendto(self.conn, "FAILED")
            data1=" STORE "+valuepair[1]+" "+valuepair[2]



new = temp()
new.start()

def signal_handler(signal, frame):
    delete_proposer(TCP_PORT)
    exit(0)

signal.signal(signal.SIGINT, signal_handler)
print('Press Ctrl+C')
forever = Event()
forever.wait()

