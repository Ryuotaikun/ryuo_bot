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

def main(): # TODO: implement multithreading and init funktion

    console.info("RyuoBot running...")

    multi.chatbot(cfg.CHAN).start()

main()
