import socket
import output
import encode_decode
from test import *

class client:
    def __init__(self):
        pass

    def connect_Proposer(self,port):
        s = socket.socket()
        ip = "127.0.0.1"
        s.connect((ip,port))
        retval = encode_decode.recvfrom(s)
        print(retval)
        return s

    def close_Proposer(self,socket):
        socket.close()

    def connect_Learner(self,port):
        s = socket.socket()
        s.connect(('127.0.0.1', port))
        retval = encode_decode.recvfrom(s)
        print(retval)
        return s

if __name__ == "__main__":
    c = client()
    Proposer_socket = []
    Learner_socket =  []
    connected_to_proposer = 0

    while(True):
        print(":::::::::::PAXOS CLIENT:::::::::::")
        print("Choose accordingly")
        print("1: Connect to the proposer")
        print("2: Write a value for the Proposer")
        print("3: Disconnect from the Proposer")
        print("4: Connect to the Learner")
        print("5: Read a value from the Learner")
        print("6: Disconnect from the Learner")
        print("7: EXIT")
        choice = input()

        if choice =='1':
            result = get_proposers()
            for i in result:
                try:
                    Proposer_socket.append(c.connect_Proposer(i[1]))
                    connected_to_proposer=1
                except ConnectionRefusedError:
                    continue

        if choice == '2':
            if connected_to_proposer == 0:
                print("FIRST CONNECT TO PROPOSER!!")
            else:
                print("insert a key value pair")
                key = input("key::   ")
                value = input("value::   ")
                string = "STORE "+key+" "+value
                for fd in Proposer_socket:
                    encode_decode.sendto(fd,string)
                retval=False
                for fd in Proposer_socket:
                    val = encode_decode.recvfrom(fd)
                    if val == "SUCCESS":
                        retval=retval or True
                if retval:
                    output.print_success("Stored")
                connected_to_proposer = 0


        if choice == '3':
            connected_to_proposer=0

        if choice=='4':
            print("Insert port of a Learner")
            port = int(input())
            Learner_socket =  c.connect_Learner(port)

        if choice=='5':
            print("Insert key")
            key = input("key:")
            string =  "SEARCH "+key
            encode_decode.sendto(Learner_socket,string)
            retval = encode_decode.recvfrom(Learner_socket)
            print(retval)

        if choice=='7':
            exit(0)
