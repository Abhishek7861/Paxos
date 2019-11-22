import socket
from threading import Thread
import output
import encode_decode
from test import *

data_store = {}

output.print_running(":::::::::::::PAXOS LEARNER:::::::::::::::")
print("Insert I.P. Address of Learner Node")
TCP_IP = input()
print("Insert Port number of Learner Node")
TCP_PORT = int(input())
insert_learner(TCP_IP,TCP_PORT)

tcpServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcpServer.bind((TCP_IP, TCP_PORT))
threads = []

while True:
    tcpServer.listen(5)
    output.print_running("Listening ...")
    (conn, (ip, port)) = tcpServer.accept()
    print("got connection from ", ip, port)
    conn.send(b"SUCCESS")
    try:
        data = encode_decode.recvfrom(conn)
    except ConnectionResetError:
        print("Connection closed by client")
    print("Server received data:", data)
    print(data)
    data = data.split()
    if data[0]=="ACCEPT":
        data_store[data[2]] = data[3]
        encode_decode.sendto(conn,"STORED")
    if data[0]=="READ":
        try:
            retval = data_store[data[1]]
            output.print_failure("Key found")
            encode_decode.sendto(conn,retval)
        except KeyError:
            output.print_failure("Key not found")
            encode_decode.sendto(conn,"Key not found")

