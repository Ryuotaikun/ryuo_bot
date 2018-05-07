# cfg.py
import console
import sys
import logging
from colorama import init

logging.basicConfig(filename='ryuobot.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

# inititalize colorama and logging
init()

RATE  = (20/30)
OWNER = "ryuotaikun"

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
