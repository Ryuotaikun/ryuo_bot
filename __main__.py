# twitchbot RyuoBot

# Developed by Ryuotaikun
# With Help from iamflemming

# __main__.py
import cfg
import multi
import socket
import logging
import interactions

print("RyuoBot running...")
logging.info("RyuoBot running...")

def main(): # TODO: implement multithreading and init funktion

    multi.chatbot(cfg.CHAN).start()

main()
