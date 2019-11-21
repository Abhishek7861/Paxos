import sqlite3
import output

def insert_proposer(IP,PORT,delay1):
    conn = sqlite3.connect('paxos.db')
    c = conn.cursor()
    try:
        c.execute("INSERT INTO proposers VALUES ('"+IP+"','"+str(PORT)+"','"+str(delay1)+"   ')")
    except sqlite3.IntegrityError:
        output.print_failure("Already used Port")
    conn.commit()
    c.close()

def insert_acceptor(IP,PORT):
    conn = sqlite3.connect('paxos.db')
    c = conn.cursor()
    try:
        c.execute("INSERT INTO acceptors VALUES ('"+IP+"','"+str(PORT)+"')")
    except sqlite3.IntegrityError:
        output.print_failure("Already used Port")
    conn.commit()
    c.close()


def insert_learner(IP,PORT):
    conn = sqlite3.connect('paxos.db')
    c = conn.cursor()
    try:
        c.execute("INSERT INTO learners VALUES ('"+IP+"','"+str(PORT)+"')")
    except sqlite3.IntegrityError:
        output.print_failure("Already used Port")
    conn.commit()
    c.close()

def get_proposers():
    conn = sqlite3.connect('paxos.db')
    c = conn.cursor()
    result = c.execute("SELECT * FROM proposers")
    return result
    conn.commit()
    c.close()

def get_proposers_count():
    conn = sqlite3.connect('paxos.db')
    c = conn.cursor()
    result = c.execute("SELECT count(*) FROM proposers")
    return (result.fetchone())[0]
    conn.commit()
    c.close()


def get_acceptors():
    conn = sqlite3.connect('paxos.db')
    c = conn.cursor()
    result = c.execute("SELECT * FROM acceptors")
    return result
    conn.commit()
    c.close()
def get_learners():
    conn = sqlite3.connect('paxos.db')
    c = conn.cursor()
    result = c.execute("SELECT * FROM learners")
    return result
    conn.commit()
    c.close()

conn = sqlite3.connect('paxos.db')
c = conn.cursor()
try:
    c.execute('''CREATE TABLE proposers
             (IP text,Port int  PRIMARY KEY,delay1 int )''')
    c.execute('''CREATE TABLE acceptors
             (IP text ,Port int  PRIMARY KEY )''')
    c.execute('''CREATE TABLE learners
             (IP text ,Port int  PRIMARY KEY )''')
except sqlite3.OperationalError:
    print("DATABASE READY")
c.close()

