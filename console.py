import colorama
import logging

def log(msg):
    logging.info(msg)
    print(colorama.Style.DIM + msg + colorama.Style.RESET_ALL)

def info(msg):
    logging.info(msg)
    print(colorama.Fore.GREEN + msg + colorama.Style.RESET_ALL)

def error(msg):
    logging.error(msg)
    print(colorama.Fore.RED + msg + colorama.Style.RESET_ALL)

def critical(msg):
    logging.critical(msg)
    print(colorama.Back.RED + msg + colorama.Style.RESET_ALL)
