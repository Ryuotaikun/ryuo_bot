# twitchbot RyuoBot

# Developed by Ryuotaikun
# With Help from iamflemming

# __main__.py
import cfg
import multi
import console
import interactions
import socket
import logging
from colorama import init

def main(): # TODO: implement multithreading and init funktion

    init()

    console.info("RyuoBot running...")

    multi.chatbot(cfg.CHAN).start()

main()
