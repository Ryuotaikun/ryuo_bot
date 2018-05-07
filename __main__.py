# twitchbot RyuoBot

# Developed by Ryuotaikun
# With Help from iamflemming

# __main__.py
import file
import twitch
import console
import re
import sys
import yaml
import threading as t

def main():

    file.restore()

    console.info("RyuoBot running...")

    '''
    Main Thread contains commands to control the other Threads from the console
    '''

    activeChan = "#ryuotaikun"   # standart channel to type in

    while True:

        input_string = input()

        if input_string[0] == "#":
            for entry in t.enumerate():
                if entry.getName() == input_string:
                    console.sys_info_head("RyuoBot is already connected to {}".format(input_string))
                    break
            else:
                activeChan = input_string
                file.addChannel(input_string)
                twitch.chatbot(input_string, "lurking").start()

        elif re.search ("!active", input_string) != None:
            activeChan = re.sub(r"!active ", "", input_string)

        elif input_string == "!list":
            console.sys_info_head("Currently running Threads:")
            for entry in t.enumerate():
                console.sys_info(entry.getName())

        elif re.search("!exit", input_string) != None:
            channel = re.sub(r"!exit ", "", input_string)
            for entry in t.enumerate():
                if entry.getName() == channel:
                    entry.stop()
                    file.removeChannel(channel)
                    console.sys_info_head("{} was stopped from the console".format(channel))
                    break
            else:
                console.sys_info_head("There is no Thread with the name {}!".format(channel))

        elif input_string == "!end":
            for entry in t.enumerate():
                if entry.getName() != "MainThread":
                    entry.stop()
                    console.sys_info_head("{} was stopped from the console".format(entry.getName()))
            console.sys_info("All Threads have been stopped and the program will exit!")
            sys.exit()

        else:
            for entry in t.enumerate():
                if entry.getName() == activeChan:
                    entry.send(input_string)
                    break
            else:
                console.sys_info_head("There is no connection to the active Channel")

main()
