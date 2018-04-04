# cfg.py
import sys

if len(sys.argv) == 1: sys.exit("ERROR: Enter a channel to connect to")

HOST  = "irc.chat.twitch.tv"                   # The Twitch IRC server
PORT  = 6667                                   # Always use 6667!
NICK  = "ryuobot"                              # Twitch username, lowercase
PASS  = "oauth:gkdugla3zz2hq3tzr0spu90hizgn4o" # Twitch OAuth token
CHAN  = "#" + sys.argv[1]                      # Twitch channel
RATE  = (20/30)                                # Messages per second
MOD   = False                                  # Default Moderator
DEBUG = False                                  # Default Debug

print("Connecting to " + CHAN + "...")

MOD = CHAN == "#ryuotaikun"                    # moderator for own channel
if MOD: print("Moderator Mode aktivated...")

if len(sys.argv) > 2:                          # Enables adv. console infomrations
    if sys.argv[2] == "True":
        DEBUG = True
        print("Debug Mode aktivated...")

ADMIN = [
    "ryuotaikun",
    "ryuobot"
]

GREET = [
    "( |^)lowhi( |$)",
    "( |^)hi( |$)",
    "( |^)hey( |$)",
    "( |^)o7( |$)",
    "( |^)hello( |$)"
]

CHARS = [
    "([ @]|^)ryuotaikun( |$)",
    "([ @]|^)ryuobot( |$)"
    "( |^)everyone( |$)",
    "( |^)chat( |$)"
]

PATT = [
    #r"swear",
    # ...
    #r"some_pattern"
    r"https://",
    r"www.",
    r".com", r".de", r".org", r".gov"
]

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
