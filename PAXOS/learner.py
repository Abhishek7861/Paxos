import socket
import output
import threading

class Learner:
    def __init__(self):
        pass

    def Learner_server(self,port):
        s = socket.socket()
        s.bind(('', port))
        s.listen(5)
        while True:
            output.print_running("Ready for accepting ... ")
            c, addr = s.accept()
            output.print_success('Got connection from '+str(addr))
            c.send(b'Thank you for connecting')
            c.close()

if __name__ == "__main__":
    print(":::::::::::LEARNER::::::::::")
    print("What is the port number of the Learner")
    port = int(input())

L = Learner()
t1 = threading.Thread(target=L.Learner_server(port))
t1.start()
t1.join()
