from termcolor import colored

import logging
from colorlog import ColoredFormatter


def setup_logger():
    """Return a logger with a default ColoredFormatter."""
    formatter = ColoredFormatter(
        "[%(filename)s: %(funcName)s() : %(lineno)s] [%(threadName)s] %(log_color)s %(message)s",
        datefmt=None,
        reset=True,
        log_colors={
            'DEBUG':    'cyan',
            'INFO':     'green',
            'WARNING':  'yellow',
            'ERROR':    'red',
            'CRITICAL': 'red',
        }
    )

    logger = logging.getLogger('example')
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)

    return logger




def print_success(string):
    print(colored(string,'green'))

def print_primary(string):
    print(colored(string,'blue'))

def print_failure(string):
    print(colored(string,'red'))

def print_running(string):
    print(colored(string,'yellow'))


