# twitchbot RyuoBot

# Developed by Ryuotaikun
# With Help from iamflemming

# __main__.py
import priv
import cfg
import socket
import re
import time
import logging
import interactions
import multi

# open socket
sock = interactions.openSocket()
# connect to initial channel
interactions.connectChannel(sock, cfg.CHAN)

print("RyuoBot running...")
logging.info("RyuoBot running...")

def main(): # TODO: implement multithreading and init funktion

    readBuffer = ""
    permittedUser = []
    alreadyGreeted = [cfg.OWNER]

    while True:

        readBuffer = readBuffer + sock.recv(4096).decode()
        messageList = readBuffer.split("\n")
        readBuffer = messageList.pop()

        for bitMessage in messageList:

            logging.debug(bitMessage)

            # Ping to Twitch
            if bitMessage == "PING :tmi.twitch.tv":
                sock.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))

            elif re.search("PRIVMSG", bitMessage) != None:

            # @badges=<badges>;color=<color>;display-name=<display-name>;emotes=<emotes>;id=<id-of-msg>;mod=<mod>;room-id=<room-id>;subscriber=<subscriber>;tmi-sent-ts=<timestamp>;turbo=<turbo>;user-id=<user-id>;user-type=<user-type> :<user>!<user>@<user>.tmi.twitch.tv PRIVMSG #<channel> :<message>

                dataList = bitMessage.split(";")

                if re.search("bits", dataList[1]) != None: # bits message
                    pass
                else:
                    if re.search("moderator", dataList[0]) != None:
                        display_name = re.sub("display-name=", "", dataList[4])
                        mod = (re.sub("mod=", "", dataList[5]) == 1)
                        subscriber = (re.sub("subscriber=", "", dataList[8]) == 1)
                    else:
                        display_name = re.sub("display-name=", "", dataList[2])
                        mod = (re.sub("mod=", "", dataList[5]) == 1)
                        subscriber = (re.sub("subscriber=", "", dataList[7]) == 1)

                    message_index = 11
                    if dataList[1] == "emote-only=1":
                        message_index = 12

                    if (re.sub("user-type=", "", dataList[message_index])[0]) == " ":
                        CHAT_MSG = re.compile(r"^\w+-\w+= :\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :")
                    else:
                        CHAT_MSG = re.compile(r"^\w+-\w+=\w+ :\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :")

                    message = CHAT_MSG.sub("", dataList[message_index])

                    print("{:<20}: {}".format(display_name, message))

                    if display_name == "Ryuotaikun" or mod == True:
                        if re.search("!ryuo off", message):
                            interactions.disconnectChannel(sock, "#lowkotv")


            #elif re.search("USERNOTICE", bitMessage) != None:


            #elif re.search("USERSTATE", bitMessage) != None:


            #elif re.search("")

            else:
                username = bitMessage
                message = bitMessage
                #if re.search("PRIVMSG", message) != None:
                #    message = CHAT_MSG.sub("", bitMessage)

                print(message)

                # TODO: Create a yaml file for commands. Implement custom commands created in chat

                if username == cfg.OWNER and re.search("!connect new ", message) != None:
                    newChannel = re.sub("!connect new ", "", message)
                    enterNewChannel(newChannel)

                elif username == cfg.OWNER and re.search("lowVe", message) != None and re.search("lowHeart", message) != None:
                    interactions.chat(sock, "<3 <3 ")

                elif username == cfg.OWNER and re.search("KAPOW", message) != None:
                    interactions.chat(sock, "KAPOW")

                elif username == cfg.OWNER and re.search("lowAim", message) != None:
                    interactions.chat(sock, "lowBlind")

                elif username == cfg.OWNER and re.search("lowBlind", message) != None:
                    interactions.chat(sock, "lowAim")

                # Greets every user greeting the owner once
                '''
                for greetings in cfg.GREET:
                    for character in cfg.CHARS:
                        if re.search(greetings, message.lower()) != None and re.search(character, message.lower()) != None and username not in alreadyGreeted:
                            interactions.chat(sock, "Hey " + username + " <3")
                            alreadyGreeted.append(username)
                            break
                '''

                ################
                # MOD COMMANDS #
                ################

                # This part will only run if the Bot is set as Admin in cfg and it
                # is actually a twitch mod in the connected channel.

                if cfg.MOD:

                    # timeout bad words and links
                    for pattern in cfg.PATT :
                        if pattern in message:
                            if username not in permittedUser:
                                print("link detected")
                                interactions.timeout(sock, username, 1)
                                print("user -" + username + "- timed out")
                                interactions.chat(sock, username + " please ask for permission before posting links.")
                                break
                            elif username in permittedUser:
                                permittedUser.remove(username)
                                break

                    # handle commands available to all viewers
                    if re.search("!drops", message) != None:
                        interactions.chat(sock, "Make sure you have Battlenet connected to Twitch to get free ingame loot while watching SC2, SC:R and SC streams: https://www.starcraft2.com/en-/us/news/21590508 SC20protoss")

                    if re.search("!mmr", message) != None:
                        interactions.chat(sock, "EU: 4050; NA: 3400 (provisional) SC20zerg")

                    if re.search("!donation", message) != None or re.search ("!tip", message) != None:
                        interactions.chat(sock, "If you feel like having too much money you can take the weight off by donating a small amount: https://www.streamlabs.com/ryuotaikun SC20zerg SC20terran")

                    # permit users to post links
                    if re.search("!permit", message) != None and username in cfg.ADMIN:
                        userToPermit = re.sub("!permit ", "", message)[:-2]
                        permittedUser.append(userToPermit)
                        print("user -" + userToPermit + "- got permisson to post a link.")
                        interactions.chat(s, userToPermit + " has permission to post a link.")

        # make sure the bot doesn't get banned for spamming
        time.sleep(1/cfg.RATE)

def enterNewChannel(channel):
    print("Trying to connect to {}".format(channel))
    #interactions.connect(s, channel)

main()
