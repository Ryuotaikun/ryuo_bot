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
                print("PONG")

            # Handle Private Messages

            elif re.search("PRIVMSG", bitMessage) != None:

            # @badges=<badges>;color=<color>;display-name=<display-name>;emotes=<emotes>;id=<id-of-msg>;mod=<mod>;room-id=<room-id>;subscriber=<subscriber>;tmi-sent-ts=<timestamp>;turbo=<turbo>;user-id=<user-id>;user-type=<user-type> :<user>!<user>@<user>.tmi.twitch.tv PRIVMSG #<channel> :<message>
                CHAT_MSG_COMPILE = re.compile(r":\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :")

                msgInfo, msgSpace, msgContent = bitMessage.partition(" ")

                attrDict = {}
                for attribute in msgInfo.split(";"):
                    key, sep, value = attribute.partition("=")
                    attrDict[key] = value

                logging.debug(msgInfo)

                username = msgContent.split("!")[0][1:]
                message = CHAT_MSG_COMPILE.sub("", msgContent)

                logging.info("{:<20}: {}".format(username, message))
                print("{:<20}: {}".format(username, message))

                # TODO: Create a yaml file for commands. Implement custom commands created in chat

                if re.search("!ryuo exit", message) != None:
                    if username == "nukeofficial":
                        interactions.chat(sock, "I don't take commands from a pleb like NukeOfficial WutFace")
                    elif username == cfg.OWNER or username == cfg.CHAN[1:] or attrDict["mod"] == "1":
                        interactions.disconnectChannel(sock, cfg.CHAN)

                if username == cfg.OWNER and re.search("!connect new ", message) != None:
                    newChannel = "#" + re.sub("!connect new ", "", message)
                    interactions.connectChannel(sock, newChannel)

                # fun commands for me

                if username == cfg.OWNER and re.search("lowVe", message) != None and re.search("lowHeart", message) != None:
                    interactions.chat(sock, "<3 <3 ")

                elif username == cfg.OWNER and re.search("KAPOW", message) != None:
                    interactions.chat(sock, "KAPOW")

                elif username == cfg.OWNER and re.search("lowAim", message) != None:
                    interactions.chat(sock, "lowBlind")

                elif username == cfg.OWNER and re.search("lowBlind", message) != None:
                    interactions.chat(sock, "lowAim")

                elif re.search("!ryuos wive", message) != None:
                    interactions.chat(sock, "That's rushIchiroSC2 of course <3")

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

                    # permit users to post links
                    if re.search("!permit", message) != None and username in cfg.ADMIN:
                        userToPermit = re.sub("!permit ", "", message)[:-2]
                        permittedUser.append(userToPermit)
                        print("user -" + userToPermit + "- got permisson to post a link.")
                        interactions.chat(s, userToPermit + " has permission to post a link.")

                    # handle commands available to all viewers
                    if re.search("!mmr", message) != None:
                        interactions.chat(sock, "EU: 4150; NA: 3400 (provisional)")

                    if re.search("!donation", message) != None or re.search ("!tip", message) != None:
                        interactions.chat(sock, "If you feel like having too much money you can take the weight off by donating a small amount: https://www.streamlabs.com/ryuotaikun")

            # Handle User Informations

            elif re.search("USERNOTICE", bitMessage) != None:

                CHAT_NOTICE_COMPILE = re.compile(r"\.tmi\.twitch\.tv USERNOTICE #\w+ :")

                noticeInfo, noticeSpace, noticeContent = bitMessage.partition(" ")

                attrDict = {}
                for attribute in noticeInfo.split(";"):
                    key, sep, value = attribute.partition("=")
                    attrDict[key] = value

                display_name = attrDict["display-name"]
                sub_type = attrDict["msg-id"]
                sub_tier = attrDict["msg-param-sub-plan"]

                if sub_type == "sub":
                    #interactions.chat(sock, "Thank you for your sub {}! KAPOW".format(display_name))
                    interactions.chat(sock, "KAPOW")

                elif sub_type == "resub":
                    sub_duration = int(attrDict["msg-param-months"])
                    if sub_duration > 10:
                        sub_duration = 10
                    #interactions.chat(sock, "Thank you for your {} months resub {}! KAPOW".format(sub_duration, display_name))
                    interactions.chat(sock, sub_duration * "KAPOW ")

                elif sub_type == "subgift":
                    sub_recipient = attrDict["msg-param-recipient-user-name"]
                    #interactions.chat(sock, "Thank you {} for gifting a sub to {}! KAPOW".format(display_name, sub_recipient))
                    interactions.chat(sock, "KAPOW")

            # Handle User Informations

            elif re.search("USERSTATE", bitMessage) != None:
                pass

            # Handle Channel Informations

            elif re.search("ROOMSTATE", bitMessage) != None:
                pass

            # Handle Channel Informations

            elif re.search("MODE", bitMessage) != None:
                pass

            # Handle Users Joining/Disconnecting

            elif re.search("JOIN", bitMessage) != None or re.search("PART", bitMessage) != None:
                #if re.search("JOIN", bitMessage) and re.search("ryuotaikun", bitMessage):
                #    interactions.chat(sock, "All hail the god of social incompetence, Ryuotaikun! DendiFace")
                pass

            # Printing all other Messages for Debugging

            else:
                print(bitMessage)

        # make sure the bot doesn't get banned for spamming
        time.sleep(1/cfg.RATE)

main()
