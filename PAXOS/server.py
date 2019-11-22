import signal
import sys
import time
from threading import *

class temp(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        while (1):
            time.sleep(2)
            print("hello")


new = temp()
new.start()

def signal_handler(signal, frame):
    print('You pressed Ctrl+C!')
    exit(0)

signal.signal(signal.SIGINT, signal_handler)
print('Press Ctrl+C')
forever = Event()
forever.wait()
