import sqlite3
import output

def insert_proposer(IP,PORT):
    conn = sqlite3.connect('paxos.db')
    c = conn.cursor()
    try:
        c.execute("INSERT INTO proposers VALUES ('"+IP+"','"+str(PORT)+"')")
    except sqlite3.IntegrityError:
        # output.print_failure("Already used Port")
        pass
    conn.commit()
    c.close()

def insert_acceptor(IP,PORT):
    conn = sqlite3.connect('paxos.db')
    c = conn.cursor()
    try:
        c.execute("INSERT INTO acceptors VALUES ('"+IP+"','"+str(PORT)+"')")
    except sqlite3.IntegrityError:
        pass
        # output.print_failure("Already used Port")
    conn.commit()
    c.close()


def insert_learner(IP,PORT):
    conn = sqlite3.connect('paxos.db')
    c = conn.cursor()
    try:
        c.execute("INSERT INTO learners VALUES ('"+IP+"','"+str(PORT)+"')")
    except sqlite3.IntegrityError:
        pass
        # output.print_failure("Already used Port")
    conn.commit()
    c.close()

def get_proposers():
    conn = sqlite3.connect('paxos.db')
    c = conn.cursor()
    result = c.execute("SELECT * FROM proposers")
    # conn.commit()
    # c.close()
    return result

def get_proposers_count():
    conn = sqlite3.connect('paxos.db')
    c = conn.cursor()
    result = c.execute("SELECT count(*) FROM proposers")
    return (result.fetchone())[0]

def get_learners_count():
    conn = sqlite3.connect('paxos.db')
    c = conn.cursor()
    result = c.execute("SELECT count(*) FROM learners")
    return (result.fetchone())[0]


def delete_proposer(port):
    conn = sqlite3.connect('paxos.db')
    c = conn.cursor()
    result = c.execute("DELETE  FROM Proposers WHERE Port = '"+str(port)+"';")
    conn.commit()
    c.close()


def get_acceptors():
    conn = sqlite3.connect('paxos.db')
    c = conn.cursor()
    result = c.execute("SELECT * FROM acceptors")
    # conn.commit()
    # c.close()
    return result

def get_learners():
    conn = sqlite3.connect('paxos.db')
    c = conn.cursor()
    result = c.execute("SELECT * FROM learners")
    # conn.commit()
    # c.close()
    return result





conn = sqlite3.connect('paxos.db')
c = conn.cursor()
try:
    c.execute('''CREATE TABLE proposers
             (IP text,Port int  PRIMARY KEY)''')
    c.execute('''CREATE TABLE acceptors
             (IP text ,Port int  PRIMARY KEY )''')
    c.execute('''CREATE TABLE learners
             (IP text ,Port int  PRIMARY KEY )''')
except sqlite3.OperationalError:
    pass
c.close()
