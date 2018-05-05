import colorama
import logging

'''
console.py colors messages in the console to make them easier to read and
sets a logging level for the logfile
'''

# info notifications (normal log and messages)

def log(msg):
    logging.info(msg)
    print(colorama.Style.DIM + msg + colorama.Style.RESET_ALL)

def info(msg):
    logging.info(msg)
    print(colorama.Fore.GREEN + msg + colorama.Style.RESET_ALL)

# notification settings (subscription and ban notifications)

def notification_pos(msg):
    logging.info(msg)
    print(colorama.Fore.CYAN + msg + colorama.Style.RESET_ALL)

def notification_neg(msg):
    logging.info(msg)
    print(colorama.Fore.YELLOW + msg + colorama.Style.RESET_ALL)

# error notifications

def error(msg):
    logging.error(msg)
    print(colorama.Fore.RED + msg + colorama.Style.RESET_ALL)

def critical(msg):
    logging.critical(msg)
    print(colorama.Back.RED + msg + colorama.Style.RESET_ALL)

# console notifications

def sys_info_head(msg):
    print(colorama.Fore.GREEN + msg + colorama.Style.RESET_ALL)

def sys_info(msg):
    print(colorama.Back.GREEN + msg + colorama.Style.RESET_ALL)
