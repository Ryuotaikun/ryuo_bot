# twitchbot RyuoBot

# Developed by Ryuotaikun
# With Help from iamflemming

# __main__.py
import priv
import cfg
import socket
import re
import time
import interactions
import multi

def main(): # TODO: implement multithreading and init funktion

    # connect to server
    s = socket.socket()
    s.connect((cfg.HOST, cfg.PORT))
    s.send("PASS {}\r\n".format(priv.PASS).encode("utf-8"))
    s.send("NICK {}\r\n".format(priv.NICK).encode("utf-8"))
    s.send("JOIN {}\r\n".format(cfg.CHAN).encode("utf-8"))

    readBuffer = ""
    permittedUser = []
    alreadyGreeted = [cfg.OWNER]

    while True:

        readBuffer = readBuffer + s.recv(4096).decode("utf-8")
        messageList = readBuffer.split("\r\n")
        readBuffer = messageList.pop()

        CHAT_MSG = re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :")

        for bitMessage in messageList:
            if cfg.DEBUG:

            # Ping to Twitch
            if bitMessage == "PING :tmi.twitch.tv":
                s.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))

            else:
                currentTime = "[" + time.strftime("%H:%M:%S") + "]"
                username = re.search(r"\w+", bitMessage).group(0)
                message = CHAT_MSG.sub("", bitMessage)

                if cfg.DEBUG:
                    print(currentTime + " " + username + ": " + message)

                if username == cfg.OWNER and re.search("!connect new ", message) != None:
                    newChannel = re.sub("!connect new ", "", message)
                    enterNewChannel(newChannel)

                if username == cfg.OWNER and re.search("lowVe", message) != None and re.search("lowHeart", message) != None:
                    interactions.chat(s, 10 * "<3 <3 ")

                if username == cfg.OWNER and re.search("KAPOW", message) != None:
                    interactions.chat(s, "KAPOW")

                if username == cfg.OWNER and re.search("lowAim", message) != None:
                    interactions.chat(s, "lowBlind")

                if username == cfg.OWNER and re.search("lowBlind", message) != None:
                    interactions.chat(s, "lowAim")

                # Greets every user greeting the owner once
                '''
                for greetings in cfg.GREET:
                    for character in cfg.CHARS:
                        if re.search(greetings, message.lower()) != None and re.search(character, message.lower()) != None and username not in alreadyGreeted:
                            interactions.chat(s, "Hey " + username + " <3")
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
                                interactions.timeout(s, username, 1)
                                print("user -" + username + "- timed out")
                                interactions.chat(s, username + " please ask for permission before posting links.")
                                break
                            elif username in permittedUser:
                                permittedUser.remove(username)
                                break

                    # handle commands available to all viewers
                    if re.search("!drops", message) != None:
                        interactions.chat(s, "Make sure you have Battlenet connected to Twitch to get free ingame loot while watching SC2, SC:R and SC streams: https://www.starcraft2.com/en-/us/news/21590508 SC20protoss")

                    if re.search("!mmr", message) != None:
                        interactions.chat(s, "EU: 4050; NA: 3400 (provisional) SC20zerg")

                    if re.search("!donation", message) != None or re.search ("!tip", message) != None:
                        interactions.chat(s, "If you feel like having too much money you can take the weight off by donating a small amount: https://www.streamlabs.com/ryuotaikun SC20zerg SC20terran")

                    # permit users to post links
                    if re.search("!permit", message) != None and username in cfg.ADMIN:
                        userToPermit = re.sub("!permit ", "", message)[:-2]
                        permittedUser.append(userToPermit)
                        print("user -" + userToPermit + "- got permisson to post a link.")
                        interactions.chat(s, userToPermit + " has permission to post a link.")

        # make sure the bot doesn't get banned for spamming
        time.sleep(1/cfg.RATE)

def enterNewChannel(channel):
    if channel == "ryuotaikun":
        interactions.chat(s, "you cant use functions you didnt implement LUL")
    else:
        interactions.chat(s, "failed to connect to #" + channel + " WutFace")

main()
