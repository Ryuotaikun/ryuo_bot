import cfg
import console
import interactions
import re
import sys
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

    # stop the thread from outside

    def stop(self):
        self.active = False
        time.sleep(1/cfg.RATE)
        interactions.disconnectChannel(self.sock, self.chan)
        interactions.closeSocket(self.sock)

    # main function of the thread

    def run(self):

        interactions.connectChannel(self.sock, self.chan)

        while self.active:

            try:
                self.readBuffer = self.readBuffer + self.sock.recv(4096).decode()
                self.messageList = self.readBuffer.split("\r\n")
                self.readBuffer = self.messageList.pop()
            except socket.timeout:
                self.messageList = []

            for bitMessage in self.messageList:

                logging.debug(bitMessage)

                # Ping to Twitch

                if bitMessage == "PING :tmi.twitch.tv":
                    self.sock.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))

                # Handle Private Messages

                elif re.search("PRIVMSG", bitMessage) != None:

                    CHAT_MSG_COMPILE = re.compile(r":\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :")

                    msgInfo, msgSpace, msgContent = bitMessage.partition(" ")

                    attrDict = {}
                    for attribute in msgInfo.split(";"):
                        key, sep, value = attribute.partition("=")
                        attrDict[key] = value

                    logging.debug(msgInfo)

                    username = msgContent.split("!")[0][1:]
                    message = CHAT_MSG_COMPILE.sub("", msgContent)

                    console.log("{:<11} - {:<10}: {}".format(self.chan[:11], username[:10], message))

                    # TODO: Create a yaml file for commands. Implement custom commands created in chat

                    if re.search("!ryuo exit", message) != None:
                        if username == "nukeofficial":
                            interactions.chat(self.sock, self.chan, "I don't take commands from a pleb like NukeOfficial WutFace")
                        elif username == cfg.OWNER or username == self.chan[1:] or attrDict["mod"] == "1":
                            chat(self.sock, self.chan, "good night everyone <3")
                            self.active = False
                            time.sleep(1/cfg.RATE)
                            interactions.disconnectChannel(self.sock, self.chan)
                            interactions.closeSocket(self.sock)

                    elif re.search("!ryuo mute", message) != None:
                        if username == cfg.OWNER or username == self.chan[1:] or attrDict["mod"] == "1":
                            if self.chan in cfg.ACCEPTED:
                                cfg.ACCEPTED.remove(self.chan)
                                console.info("{:<24}: RyuoBot is no longer allowed to type in this channel!".format(self.chan))

                    elif re.search("!ryuo unmute", message) != None:
                        if username == cfg.OWNER or username == self.chan[1:] or attrDict["mod"] == "1":
                            if self.chan not in cfg.ACCEPTED:
                                cfg.ACCEPTED.append(self.chan)
                                console.info("{:<24}: RyuoBot is now allowed to type in this channel!".format(self.chan))

                    if username == cfg.OWNER and re.search("!connect new ", message) != None:
                        newChannel = "#" + re.sub("!connect new ", "", message)
                        chatbot(newChannel).start()

                    # fun commands for me

                    elif username == cfg.OWNER and re.search("KAPOW", message) != None:
                        interactions.chat(self.sock, self.chan, "KAPOW")

                    elif re.search("!ryuos wife", message) != None:
                        interactions.chat(self.sock, self.chan, "That's rushIchiroSC2 of course <3")

                    ################################
                    # MOD COMMANDS FOR #RYUOTAIKUN #
                    ################################

                    if self.chan == "#ryuotaikun":

                        # timeout bad words and links
                        for pattern in cfg.PATT :
                            if pattern in message:
                                if username not in permittedUser:
                                    console.info("{:<24}: link detected".format(self.chan[:24]))
                                    interactions.timeout(self.sock, self.chan, username, 1)
                                    console.info("{:<24}: user -{}- timed out".format(self.chan[:24], username))
                                    interactions.chat(self.sock, self.chan, username + " please ask for permission before posting links.")
                                    break
                                elif username in permittedUser:
                                    permittedUser.remove(username)
                                    break

                        # permit users to post links
                        if re.search("!permit", message) != None and username in cfg.ADMIN:
                            userToPermit = re.sub("!permit ", "", message)[:-2]
                            permittedUser.append(userToPermit)
                            console.info("{:<24}: user -{}- got permisson to post a link.".format(self.chan[:24], username))
                            interactions.chat(self.sock, self.chan, "{} has permission to post a link.".format(userToPermit))

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
                        console.notification_pos("{:<24}: {} just subscribed!".format(self.chan[:24], display_name))
                        interactions.chat(self.sock, self.chan, "KAPOW")

                    elif sub_type == "resub":
                        sub_duration = int(attrDict["msg-param-months"])
                        console.notification_pos("{:<24}: {} just resubed for {} months!".format(self.chan[:24], display_name, sub_duration))
                        #interactions.chat(self.sock, "Thank you for your {} months resub {}! KAPOW".format(sub_duration, display_name))
                        interactions.chat(self.sock, self.chan, sub_duration//12 * "lowS " + sub_duration%12 * "KAPOW ")

                    elif sub_type == "subgift":
                        sub_recipient = attrDict["msg-param-recipient-user-name"]
                        #interactions.chat(self.sock, "Thank you {} for gifting a sub to {}! KAPOW".format(display_name, sub_recipient))
                        console.notification_pos("{:<24}: {} just gifted a subscription to {}!".format(self.chan[:24], display_name, sub_recipient))
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

                elif re.search("CLEARCHAT", bitMessage) != None:

                    BAN_MSG_COMPILE = re.compile(r":tmi\.twitch\.tv CLEARCHAT #\w+ :")

                    banInfo, banSpace, banContent = bitMessage[1:].partition(" ")

                    username = BAN_MSG_COMPILE.sub("", banContent)

                    console.notification_neg("{:<24}: {} just got banned from {}!".format(self.chan[:24], username, self.chan))

                # Printing all other Messages for Debugging

                else:
                    logging.info(bitMessage)
                    print(bitMessage)

            # Force python to print everything in the buffer
            sys.stdout.flush()

            # make sure the bot doesn't get banned for spamming
            time.sleep(1/cfg.RATE)
