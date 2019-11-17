from termcolor import colored

def print_success(string):
    print(colored(string,'green'))

def print_primary(string):
    print(colored(string,'blue'))

def print_failure(string):
    print(colored(string,'red'))

def print_running(string):
    print(colored(string,'yellow'))
