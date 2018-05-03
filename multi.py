import cfg
import priv
import interactions
import re
import time
import socket
import logging
from threading import Thread

class chatbot(Thread):

    def __init__(self, chan):
        Thread.__init__(self)
        self.active = True
        self.sock = interactions.openSocket()
        self.setName(chan)
        self.chan = chan
        self.readBuffer = ""
        self.permittedUser = []

    def run(self):

        interactions.connectChannel(self.sock, self.chan)

        while self.active:

            self.readBuffer = self.readBuffer + self.sock.recv(4096).decode()
            self.messageList = self.readBuffer.split("\n")
            self.readBuffer = self.messageList.pop()

            for bitMessage in self.messageList:

                logging.debug(bitMessage)

                # Ping to Twitch
                if bitMessage == "PING :tmi.twitch.tv":
                    self.sock.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
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

                    logging.info("{:<11} - {:<10}: {}".format(self.chan[:11], username[:10], message))
                    print("{:<11} - {:<10}: {}".format(self.chan[:11], username[:10], message))

                    # TODO: Create a yaml file for commands. Implement custom commands created in chat

                    if re.search("!ryuo exit", message) != None:
                        if username == "nukeofficial":
                            interactions.chat(self.sock, "I don't take commands from a pleb like NukeOfficial WutFace")
                        elif username == cfg.OWNER or username == self.chan[1:] or attrDict["mod"] == "1":
                            interactions.disconnectChannel(self.sock, self.chan)
                            interactions.closeSocket(self.sock)
                            self.active = False

                    if username == cfg.OWNER and re.search("!connect new ", message) != None:
                        newChannel = "#" + re.sub("!connect new ", "", message)
                        chatbot(newChannel).start()

                    # fun commands for me

                    if username == cfg.OWNER and re.search("lowVe", message) != None and re.search("lowHeart", message) != None:
                        interactions.chat(self.sock, self.chan, "<3 <3 ")

                    elif username == cfg.OWNER and re.search("KAPOW", message) != None:
                        interactions.chat(self.sock, self.chan, "KAPOW")

                    elif username == cfg.OWNER and re.search("lowAim", message) != None:
                        interactions.chat(self.sock, self.chan, "lowBlind")

                    elif username == cfg.OWNER and re.search("lowBlind", message) != None:
                        interactions.chat(self.sock, self.chan, "lowAim")

                    elif re.search("!ryuos wive", message) != None:
                        interactions.chat(self.sock, self.chan, "That's rushIchiroSC2 of course <3")

                    ################################
                    # MOD COMMANDS FOR #RYUOTAIKUN #
                    ################################

                    if self.chan == "#ryuotaikun\r":

                        # timeout bad words and links
                        for pattern in cfg.PATT :
                            if pattern in message:
                                if username not in permittedUser:
                                    print("link detected")
                                    interactions.timeout(self.sock, username, 1)
                                    print("user -" + username + "- timed out")
                                    interactions.chat(self.sock, self.chan, username + " please ask for permission before posting links.")
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

                        # handle commands available to all viewers in my own channel
                        if re.search("!mmr", message) != None:
                            interactions.chat(self.sock, self.chan, "EU: 4150; NA: 3400 (provisional)")

                        if re.search("!donation", message) != None or re.search ("!tip", message) != None:
                            interactions.chat(self.sock, self.chan, "If you feel like having too much money you can take the weight off by donating a small amount: https://www.streamlabs.com/ryuotaikun")

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
                        #interactions.chat(self.sock, "Thank you for your sub {}! KAPOW".format(display_name))
                        interactions.chat(self.sock, self.chan, "KAPOW")

                    elif sub_type == "resub":
                        sub_duration = int(attrDict["msg-param-months"])
                        if sub_duration > 10:
                            sub_duration = 10
                        #interactions.chat(self.sock, "Thank you for your {} months resub {}! KAPOW".format(sub_duration, display_name))
                        interactions.chat(self.sock, self.chan, sub_duration * "KAPOW ")

                    elif sub_type == "subgift":
                        sub_recipient = attrDict["msg-param-recipient-user-name"]
                        #interactions.chat(self.sock, "Thank you {} for gifting a sub to {}! KAPOW".format(display_name, sub_recipient))
                        interactions.chat(self.sock, self.chan, "KAPOW")

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
                    #    interactions.chat(self.sock, "All hail the god of social incompetence, Ryuotaikun! DendiFace")
                    pass

                # Printing all other Messages for Debugging

                else:
                    print(bitMessage)

            # make sure the bot doesn't get banned for spamming
            time.sleep(1/cfg.RATE)
