# cfg.py
import console
import sys
import logging
from colorama import init

def debug():
    if len(sys.argv) > 1:                      # Setting logging level
        if sys.argv[1] == "True":
            logging.basicConfig(filename='ryuobot.log', level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(message)s')
            console.info("Debug Mode activated")
    else:
        logging.basicConfig(filename='ryuobot.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

# inititalize colorama and logging
init()
debug()

HOST  = "irc.chat.twitch.tv"                   # The Twitch IRC server
PORT  = 6667                                   # Always use 6667!
RATE  = (20/30)                                # Messages per second
DEBUG = False                                  # Default Debug
OWNER = "ryuotaikun"                           # Set your Twitch Name

# TODO: Move PATT and ACCEPTED in a json file

PATT = [                                       # patterns to time out
    # make sure to prefix quotes with an 'r' to make re handle . , - etc!
    r"https://",
    r"www.",
    r".com", r".de", r".org", r".gov"
]

ACCEPTED = [                                   # list of channels in which The
    "#ryuotaikun",                             # the bot is allowed to type
    "#lowkotv",
    "#rushIchiroSC2"
]
