# cfg.py
import sys
import logging

# check arguments given
if len(sys.argv) == 1:
    print("CRITICAL ERROR: Missing channel to connect!")
    logging.critical("Missing channel to connect!")
    sys.exit()

#NICK  =  Twitch username, lowercase
#PASS  =  Twitch OAuth token

HOST  = "irc.chat.twitch.tv"                   # The Twitch IRC server
PORT  = 6667                                   # Always use 6667!
CHAN  = "#" + sys.argv[1]                      # Twitch channel
RATE  = (20/30)                                # Messages per second
MOD   = False                                  # Default Moderator
DEBUG = False                                  # Default Debug
OWNER = "ryuotaikun"                           # Set your Twitch Name

if len(sys.argv) > 2:                          # Setting logging level
    if sys.argv[2] == "True":
        logging.basicConfig(filename='test.log', level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(message)s')
        print("Debug Mode activated")
        logging.info("Debug Mode aktivated")
else:
    logging.basicConfig(level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

logging.info("Connecting to {}".format(CHAN))

MOD = CHAN == '#'+OWNER                        # moderator for own channel
if MOD: logging.info("Moderator Mode aktivated")

ADMIN = [                                      # users allowed to use admin commands
    "ryuotaikun",
    "ryuobot"
]

GREET = [                                      # greetings to react to
    "( |^)lowhi( |$)",                         # ^ and $ for message start/end
    "( |^)hi( |$)",
    "( |^)hey( |$)",
    "( |^)o7( |$)",
    "( |^)hello( |$)"
]

CHARS = [                                      # chars to react to
    "([ @]|^)ryuotaikun( |$)",
    "([ @]|^)ryuobot( |$)"
    "( |^)everyone( |$)",
    "( |^)chat( |$)"
]

PATT = [                                       # patterns to time out
    # make sure to prefix quotes with an 'r' to make re handle . , - etc!
    r"https://",
    r"www.",
    r".com", r".de", r".org", r".gov"
]

# tested this in the ubuntu terminal. does not work in the windows cmd
COLOR = {
    # font colors
    'black': '\033[90m',
    'red': '\033[91m',
    'green': '\033[92m',
    'yellow': '\033[93m',
    'blue': '\033[94m',
    'magenta': '\033[95m',
    'cyan': '\033[96m',
    'white': '\033[97m',
    # backgound colors
    'b_black': '\033[40m',
    'b_red': '\033[41m',
    'b_green': '\033[42m',
    'b_yellow': '\033[43m',
    'b_blue': '\033[44m',
    'b_magenta': '\033[45m',
    'b_cyan': '\033[46m',
    'b_white': '\033[47m',
    # end
    'end': '\033[0m'
}
