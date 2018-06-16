# twitchbot RyuoBot

# Developed by Ryuotaikun
# With Help from iamflemming

# __main__.py
import file
import twitch
import console
import discordBot
import re
import sys
import time
import asyncio
import discord
import threading as t

def main():

    console.info("RyuoBot starting...")

    client = discord.Client(loop=asyncio.new_event_loop())
    discordBot.discordbot(client).start()

    time.sleep(.1)

    console.info("Connected to Discord.")

    file.restore()

    time.sleep(.1)

    console.info("Reconnected to Twitch.")

    console.info("RyuoBot running...")

    '''
    Main Thread contains commands to control the other Threads from the console
    '''

    activeChan = "#ryuotaikun"   # standart channel to type in

    while True:

        input_string = input()

        if len(input_string) > 0 and input_string[0] == "#":
            for entry in t.enumerate():
                if entry.getName() == input_string:
                    console.sys_info_head("RyuoBot is already connected to {}".format(input_string))
                    break
            else:
                activeChan = input_string
                file.addChannel(input_string)
                twitch.twitchbot(input_string, "lurking").start()

        elif re.search ("!active", input_string) != None:
            activeChan = re.sub(r"!active ", "", input_string)

        elif re.search ("!status active", input_string) != None:
            chan = re.sub(r"!status active ", "", input_string)
            file.updateStatus(chan, "active")


        elif re.search ("!verify", input_string) != None:
            chan = re.sub(r"!verify ", "", input_string)
            file.updateStatus(chan, "verified")

        elif input_string == "!list":
            console.sys_info_head("Currently running Threads:")
            for entry in t.enumerate():
                console.sys_info(entry.getName())

        elif re.search("!exit", input_string) != None:
            channel = re.sub(r"!exit ", "", input_string)
            for entry in t.enumerate():
                if entry.getName() == channel:
                    entry.stop()
                    console.sys_info_head("{} was stopped from the console".format(channel))
                    break
            else:
                console.sys_info_head("There is no Thread with the name {}!".format(channel))

        # TODO: implement Discord exit in console

        elif input_string == "!end":
            client.logout()
            for entry in t.enumerate():
                if entry.getName().startswith("#"):
                    entry.stop()
                    console.sys_info_head("{} was stopped from the console".format(entry.getName()))
            console.sys_info("All Twitch Threads have been stopped and the program will exit!")
            for entry in t.enumerate():
                console.sys_info(entry.getName())
            sys.exit()
            for entry in t.enumerate():
                console.sys_info(entry.getName())

        else:
            for entry in t.enumerate():
                if entry.getName() == activeChan:
                    entry.send(input_string)
                    break
            else:
                console.sys_info_head("There is no connection to the active Channel")

main()
