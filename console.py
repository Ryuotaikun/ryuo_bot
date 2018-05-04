import colorama
import logging

'''
console.py colors messages in the console to make them easier to read and
set a logging level for the logfile
'''

def log(msg):
    logging.info(msg)
    print(colorama.Style.DIM + msg + colorama.Style.RESET_ALL)

def info(msg):
    logging.info(msg)
    print(colorama.Fore.GREEN + msg + colorama.Style.RESET_ALL)

def notification(msg):
    logging.info(msg)
    print(colorama.Fore.BLUE + msg + colorama.Style.RESET_ALL)

def error(msg):
    logging.error(msg)
    print(colorama.Fore.RED + msg + colorama.Style.RESET_ALL)

def critical(msg):
    logging.critical(msg)
    print(colorama.Back.RED + msg + colorama.Style.RESET_ALL)
