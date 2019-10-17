import socket
import output
import encode_decode

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
        print(s.recv(1024))
        s.close()

if __name__ == "__main__":
    c = client()
    Proposer_socket = None
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

        if choice=='7':
            exit(0)

        if choice=='4':
            print("Insert port of a Learner")
            port = int(input())
            c.connect_Learner(port)

        if choice =='1':
            print("Insert port of a proposer to connect")
            port = int(input())
            Proposer_socket = c.connect_Proposer(port)
            connected_to_proposer=1


        if choice == '2':
            if connected_to_proposer == 0:
                print("FIRST CONNECT TO PROPOSER!!")
            else:
                print("insert a key value pair")
                key = input("key::   ")
                value = input("value::   ")
                string = "STORE "+key+" "+value
                encode_decode.sendto(Proposer_socket,string)
                retval = encode_decode.recvfrom(Proposer_socket)
                print(retval)

        if choice == '3':
            connected_to_proposer=0

