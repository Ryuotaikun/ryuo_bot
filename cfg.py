# cfg.py
import console
import sys
import logging
from colorama import init

# inititalize colorama
init()

# check arguments given
if len(sys.argv) == 1:
    console.critical("CRITICAL ERROR: Missing channel to connect!")
    sys.exit()

HOST  = "irc.chat.twitch.tv"                   # The Twitch IRC server
PORT  = 6667                                   # Always use 6667!
CHAN  = "#" + sys.argv[1]                      # Twitch channel
RATE  = (20/30)                                # Messages per second
MOD   = False                                  # Default Moderator
DEBUG = False                                  # Default Debug
OWNER = "ryuotaikun"                           # Set your Twitch Name

if len(sys.argv) > 2:                          # Setting logging level
    if sys.argv[2] == "True":
        logging.basicConfig(filename='ryuobot.log', level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(message)s')
        console.info("Debug Mode activated")
else:
    logging.basicConfig(filename='ryuobot.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

MOD = CHAN == '#'+OWNER                        # moderator for own channel
if MOD: console.info("Moderator Mode aktivated")

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
