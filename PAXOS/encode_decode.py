def recvfrom(s):
    mystring = s.recv(1024)
    b = mystring.decode('utf-8')
    return b

def sendto(s,mystring):
    b = bytes(mystring, 'utf-8')
    s.send(b)