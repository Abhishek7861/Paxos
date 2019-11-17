import socket
from threading import Thread
import output
import encode_decode
import configparser
from test import *
import random

base=0

class Proposer_Thread(Thread):
    def __init__(self, ip, port):
        Thread.__init__(self)
        self.ip = ip
        self.port = port

    def run(self):
        flag=True
        while(flag):
            try:
                data = encode_decode.recvfrom(conn)
            except ConnectionResetError:
                print("Connection closed by client")
                return
            print("Server received data:", data)
            if data is '':
                continue
                flag=False
            else:
                self.connect_acceptor(data)
                flag=False

    def connect_acceptor(self,data):
        acceptor_socket=[]
        ipport = []
        global base
        global conn
        base = base+random.randrange(1,50)
        data = "PREPARE "+str(base)
        result = get_acceptors()
        for i in result:
            s = socket.socket()
            ipport.append(i)
            acceptor_socket.append(s)
        for fd in acceptor_socket:
            i = ipport.pop()
            fd.connect((i[0],i[1]))
            retval = encode_decode.recvfrom(fd)
            output.print_running(retval)
        for fd in acceptor_socket:
            encode_decode.sendto(fd,data)
        for fd in acceptor_socket:
            retval = encode_decode.recvfrom(fd)
            output.print_running(retval)
            retval = retval.split()
        if retval[0]=='PROMISE':
            output.print_success(retval)
            data = "ACCEPT-REQUEST "+str(base)
            for fd in acceptor_socket:
                encode_decode.sendto(fd, data)
            for fd in acceptor_socket:
                retval = encode_decode.recvfrom(fd)
                print(retval)
            encode_decode.sendto(conn, "SUCCESS")
        elif retval[0]=='ACCEPT':
            base = int(retval[1])
            encode_decode.sendto(conn, "FAILED")


output.print_success(":::::::::::::PAXOS PROPOSER:::::::::::::::")
print("Insert I.P. Address of Proposer Node")
TCP_IP = input()
print("Insert Port number of Proposer Node")
TCP_PORT = int(input())
insert_proposer(TCP_IP,TCP_PORT)
tcpServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcpServer.bind((TCP_IP, TCP_PORT))
threads = []

while True:
    tcpServer.listen(5)
    output.print_running("Listening ...")
    (conn, (ip, port)) = tcpServer.accept()
    print("got connection from ",ip,port)
    conn.send(b"SUCCESS")
    newthread = Proposer_Thread(ip, port)
    newthread.start()
    threads.append(newthread)
