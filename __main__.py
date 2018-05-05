# twitchbot RyuoBot

# Developed by Ryuotaikun
# With Help from iamflemming

# __main__.py
import cfg
import multi
import console
import re
import sys
import threading as t

def main():

    console.info("RyuoBot running...")

    '''
    Main Thread contains commands to control the other Threads from the console
    '''

    while True:
        command = input()
        if command[0] == "#":
            for entry in t.enumerate():
                if entry.getName() == command:
                    console.sys_info_head("RyuoBot is already connected to {}".format(command))
                    break
            else:
                multi.chatbot(command).start()

        elif command == "!list":
            console.sys_info_head("Currently running Threads:")
            for entry in t.enumerate():
                console.sys_info(entry.getName())

        elif re.search("!exit", command) != None:
            channel = re.sub(r"!exit ", "", command)
            for entry in t.enumerate():
                if entry.getName() == channel:
                    entry.stop()
                    console.sys_info_head("{} was stopped from the console".format(channel))
                    break
            else:
                console.sys_info_head("There is no Thread with the name {}!".format(channel))

        elif command == "!end":
            for entry in t.enumerate():
                if entry.getName() != "MainThread":
                    entry.stop()
                    console.sys_info_head("{} was stopped from the console".format(entry.getName()))
            console.sys_info("All Threads have been stopped and the program will exit!")
            sys.exit()
main()
