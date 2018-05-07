import cfg
import file
import console
import interactions
import re
import sys
import time
import socket
import logging
from threading import Thread

class chatbot(Thread):

    def __init__(self, chan, mode):
        Thread.__init__(self)
        self.active = True
        self.sock = interactions.openSocket()
        self.setName(chan)
        self.chan = chan
        self.mode = mode
        self.readBuffer = ""
        self.permittedUser = []

    # stop the thread from outside

    def stop(self):
        self.active = False
        time.sleep(1/cfg.RATE)
        interactions.disconnectChannel(self.sock, self.chan)
        interactions.closeSocket(self.sock)

    # send message from MainThread

    def send(self, msg):
        interactions.chat(self.sock, self.chan, msg)

    # sending an error if a bitMessage can't be processed

    def cannotProcess(self, type, message):
        console.error("Recieved a {} that can't be processed:".format(type))
        print("-\r\n{}\r\n-".format(message))


    # main function of the thread

    def run(self):

        # get settings and commands from file

        # file.getFromFile()

        # connect to channel

        interactions.connectChannel(self.sock, self.chan)

        while self.active:

            try:
                self.readBuffer = self.readBuffer + self.sock.recv(4096).decode()
                self.messageList = self.readBuffer.split("\r\n")
                self.readBuffer = self.messageList.pop()
            except socket.timeout:
                self.messageList = []

            for bitMessage in self.messageList:

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

                    username = msgContent.split("!")[0][1:]
                    message = CHAT_MSG_COMPILE.sub("", msgContent)

                    console.log("{:<11} - {:<10}: {}".format(self.chan[:11], username[:10], message))

                    # TODO: Create a yaml file for commands. Implement custom commands created in chat

                    if re.search("!ryuo exit", message) != None:
                        if username == "nukeofficial":
                            interactions.chat(self.sock, self.chan, "I don't take commands from a pleb like NukeOfficial WutFace")
                        elif username == cfg.OWNER or username == self.chan[1:] or attrDict["mod"] == "1":
                            interactions.chat(self.sock, self.chan, "good night everyone <3")
                            self.active = False
                            time.sleep(1/cfg.RATE)
                            file.removeChannel(self.chan)
                            interactions.disconnectChannel(self.sock, self.chan)
                            interactions.closeSocket(self.sock)

                    elif re.search("!ryuo mute", message) != None:
                        if username == cfg.OWNER or username == self.chan[1:] or attrDict["mod"] == "1":
                            if self.chan in cfg.ACCEPTED:
                                cfg.ACCEPTED.remove(self.chan)
                                console.info("{:<24}: RyuoBot is no longer allowed to type in {}!".format(self.chan[:24], self.chan))

                    elif re.search("!ryuo unmute", message) != None:
                        if username == cfg.OWNER or username == self.chan[1:] or attrDict["mod"] == "1":
                            if self.chan not in cfg.ACCEPTED:
                                cfg.ACCEPTED.append(self.chan)
                                console.info("{:<24}: RyuoBot is now allowed to type in {}!".format(self.chan[:24], self.chan))

                    if username == cfg.OWNER and re.search("!connect new ", message) != None:
                        newChannel = "#" + re.sub("!connect new ", "", message)
                        chatbot(newChannel, "lurking").start()

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
                            console.info("{:<24}: user -{}- got permisson to post a link.".format(self.chan, username))
                            interactions.chat(self.sock, self.chan, "{} has permission to post a link.".format(userToPermit))

                        # handle commands available to all viewers in my own channel

                        if re.search("!song", message.lower()) != None:
                            interactions.chat(self.sock, self.chan, "How am I supposed to know. Ryuo hates spotify ¯\_(ツ)_/¯")

                        if re.search("!ryuobot", message.lower()) != None:
                            interactions.chat(self.sock, self.chan, "I am an experimental version of a Twitch Bot. Read more about me here: https://www.github.com/Ryuotaikun/ryuo_bot")

                        if re.search("!mmr", message.lower()) != None:
                            interactions.chat(self.sock, self.chan, "EU: 4150; NA: 3400 (provisional)")

                        if re.search("!donation", message.lower()) != None or re.search ("!tip", message) != None:
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

                elif re.search("NOTICE", bitMessage) != None:
                    CHAN_NOTICE_COMPILE = re.compile(r":tmi\.twitch\.tv NOTICE #\w+ :")

                    notInfo, notSpace, notContent = bitMessage.partition(" ")

                    message = CHAN_NOTICE_COMPILE.sub("", notContent)

                    if "host_on" in notInfo:
                        host_target = message.split(" ")[2][:-1]
                        console.notification_chan("{:<24}: {} is now hosting {}!".format(self.chan[:24], self.chan, host_target))

                    elif "host_off" in notInfo:
                        console.notification_chan("{:<24}: {} stopped hosting!".format(self.chan[:24], self.chan))

                    elif "host_target_went_offline" in notInfo:
                        host_target = message.split(" ")[0]
                        console.notification_chan("{:<24}: {} is no longer hosting {}!".format(self.chan[:24], self.chan, host_target))

                    else:
                        chatbot.cannotProcess(self, "PRIVMSG", bitMessage)

                # Handle Channel Informations

                elif re.search("ROOMSTATE", bitMessage) != None:
                    roomInfo, roomSpace, roomContent = bitMessage[1:].partition(" ")

                    attrDict = {}
                    for attribute in roomInfo.split(";"):
                        key, sep, value = attribute.partition("=")
                        attrDict[key] = value

                    if "r9k" in attrDict:
                        r9k = attrDict["r9k"] == "1"
                    if "slow" in attrDict:
                        slow = attrDict["r9k"] != "0"
                    if "subs-only" in attrDict:
                        subs_only = attrDict["r9k"] == "1"

                    if r9k:
                        console.notification_chan("{:<24}: {0} is in r9k mode!".format(self.chan[:24], self.chan))
                    if slow:
                        console.notification_chan("{:<24}: {0} is in slow mode!".format(self.chan[:24], self.chan))
                    if subs_only:
                        console.notification_chan("{:<24}: {0} is in subscribers only mode!".format(self.chan[:24], self.chan))

                # Handle Channel Informations

                elif re.search("MODE", bitMessage) != None:
                    pass
                    #chatbot.cannotProcess(self, "MODE", bitMessage)

                # Handle Hosting Informations

                elif re.search("HOSTTARGET", bitMessage) != None:
                    TARGET_MSG_COMPILE = re.compile(r":tmi\.twitch\.tv HOSTTARGET #\w+ :")

                    message = TARGET_MSG_COMPILE.sub("", bitMessage)

                    if message[0] == "-":
                        viewer_count = message[2:]
                        console.notification_chan("{:24}: {} stopped hosting for {} viewers!".format(self.chan[:24], self.chan, viewer_count))
                    else:
                        host_target, sep, viewer_count = message.partition(" ")
                        console.notification_chan("{:24}: {} startet hosting {} for {} viewers!".format(self.chan[:24], self.chan, host_target, viewer_count))



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
