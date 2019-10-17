import colorama
from colorama import Fore, Back, Style

def print_failure(text):
    print(Fore.RED + text)
    Style.RESET_ALL

def print_success(text):
    print(Fore.GREEN+ text)
    Style.RESET_ALL

def print_normal(text):
    print(Fore.BLACK + text)
    Style.RESET_ALL

def print_running(text):
    print(Fore.YELLOW + text)
    Style.RESET_ALL




