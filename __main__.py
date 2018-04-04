#twitchbot RyuoBot

#Developed by Ryuotaikun
#With Help from iamflemming

# __main__.py
import cfg
import socket
import re
import time
import interactions
import keyboard

s = socket.socket()
s.connect((cfg.HOST, cfg.PORT))
s.send("PASS {}\r\n".format(cfg.PASS).encode("utf-8"))
s.send("NICK {}\r\n".format(cfg.NICK).encode("utf-8"))
s.send("JOIN {}\r\n".format(cfg.CHAN).encode("utf-8"))

readBuffer = ""
permittedUser = []
alreadyGreeted = ["ryuotaikun"]
n=0

while True:

    #Make sure to prefix quotes with an 'r' to make sure re handels . , - etc!
    #if re.search(re.compile(r"^\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :"))
#if re.match("PRIVMSG", re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :")) != None:

    readBuffer = readBuffer + s.recv(4096).decode("utf-8")
    messageList = readBuffer.split("\r\n")
    readBuffer = messageList.pop()

    CHAT_MSG = re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :")
    #CHAT_SUB = re.compile()


    if keyboard.is_pressed(' ') != False:
        interactions.chat(s, input("what to send?"))

    for bitMessage in messageList:
        if cfg.DEBUG:
            print("=====================")
            print(re.sub("\r\n", "", bitMessage))
            print("=====================")

        # Ping to Twitch
        if bitMessage == "PING :tmi.twitch.tv":
            s.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))

        else:
            currentTime = cfg.COLOR['cyan'] + "[" + time.strftime("%H:%M:%S") + "]" + cfg.COLOR['end']
            username = cfg.COLOR['red'] + re.search(r"\w+", bitMessage).group(0) + cfg.COLOR['end']
            message = cfg.COLOR['blue'] + CHAT_MSG.sub("", bitMessage) + cfg.COLOR['end']
            #currentTime = "[" + time.strftime("%H:%M:%S") + "]"
            #username = re.search(r"\w+", bitMessage).group(0)
            #message = CHAT_MSG.sub("", bitMessage)
            print(currentTime + " " + username + ": " + message)

            #reacting to subscrptions
            #subscription = CHAT_SUB.sub("", bitMessage)
            #if subscription != "\r\n":
            #    print("user -" + username + "- just subscribed to the channel")

            #if re.search("KAPOW", message) != None:
            #    interactions.chat(s, "KAPOW")

            if username == "ryuotaikun" and re.search("lowVe", message) != None and re.search("lowHeart", message) != None:
                interactions.chat(s, 10 * "lowVe lowHeart ")

            if username == "ryuotaikun" and re.search("KAPOW", message) != None:
                interactions.chat(s, "KAPOW")

            if username == "ryuotaikun" and re.search("lowAim", message) != None:
                interactions.chat(s, "lowBlind")

            if username == "ryuotaikun" and re.search("lowBlind", message) != None:
                interactions.chat(s, "lowAim")

            # Greetings
            """
            for greetings in cfg.GREET:
                for character in cfg.CHARS:
                    if re.search(greetings, message.lower()) != None and re.search(character, message.lower()) != None and username not in alreadyGreeted:
                        interactions.chat(s, "lowHi " + username)
                        alreadyGreeted.append(username)
                        break
            """

            # MOD COMMANDS #
            if cfg.MOD:

                #timeout bad words and links
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

                #handle commands available to all viewers
                if re.search("!vote", message) != None:
                    interactions.chat(s, "The vote for Nation Wars V is over. You can see the results here: http://www.nationwars.tv/vote SC20terran")

                if re.search("!drops", message) != None:
                    interactions.chat(s, "Make sure you have Battlenet connected to Twitch to get free ingame loot while watching SC2, SC:R and SC streams: https://www.starcraft2.com/en-/us/news/21590508 SC20protoss")

                if re.search("!mmr", message) != None:
                    interactions.chat(s, "EU: 4050; NA: 3400 (provisional) SC20zerg")

                if re.search("!donation", message) != None or re.search ("!tip", message) != None:
                    interactions.chat(s, "If you feel like having too much money you can take the weight off by donating a small amount: https://www.streamlabs.com/ryuotaikun SC20zerg SC20terran")

                #permit users to post links
                if re.search("!permit", message) != None and username in cfg.ADMIN:
                    userToPermit = re.sub("!permit ", "", message)[:-2]
                    permittedUser.append(userToPermit)
                    print("user -" + userToPermit + "- got permisson to post a link.")
                    interactions.chat(s, userToPermit + " has permission to post a link.")

    time.sleep(1/cfg.RATE)
