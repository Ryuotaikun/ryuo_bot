import cfg
import priv
import console
import sys
import socket
import time
import logging

def openSocket():
    """
    Opens Socket
    Requests Twitch-Specific IRC Capabilities
    Keyword arguments:
    sock -- the socket to use for sending/recieving messages
    """
    sock = socket.socket()
    sock.settimeout(2)
    sock.connect((cfg.HOST, cfg.PORT))
    sock.send("PASS {}\r\n".format(priv.PASS).encode("utf-8"))
    sock.send("NICK {}\r\n".format(priv.NICK).encode("utf-8"))

    sock.send("CAP REQ :twitch.tv/membership\r\n".encode("utf-8"))
    sock.send("CAP REQ :twitch.tv/tags\r\n".encode("utf-8"))
    sock.send("CAP REQ :twitch.tv/commands\r\n".encode("utf-8"))

    return sock

def closeSocket(sock):
    """
    Closes Socket
    Keyword arguments:
    sock -- the socket to close
    """
    try:
        sock.close()
        console.info("The socket has been closed")
    except Exception as e:
        console.error("Could not close socket")

def connectChannel(sock, chan):
    """
    Connects to the Twitch IRC
    Keyword arguments:
    chan -- the channel to connect to
    sock -- the socket over which to send the join request
    """
    sock.send("JOIN {}\r\n".format(chan).encode("utf-8"))

    console.info("Successfully connected to {}".format(chan))

def disconnectChannel(sock, chan):
    """
    Disconnects from the Twitch IRC
    Keyword arguments:
    chan -- the channel from which to disconnect
    sock -- the socket over which to send the disconnect request
    """
    chat(sock, chan, "good night everyone <3")
    sock.send("PART {}\r\n".format(chan).encode("utf-8"))

    console.info("Successfully disconnected from {}".format(chan))

def chat(sock, chan, msg):
    """
    Send a chat message to the server.
    (only if the bot is allowed to type in that chan)
    Keyword arguments:
    sock -- the socket over which to send the message
    chan -- the channel to send the message to
    msg  -- the message to be send
    """
    if chan in cfg.ACCEPTED:
        sock.send("PRIVMSG {} :{}\r\n".format(chan, msg).encode("utf-8"))
        console.info("{:<11} - {:<10}: {}".format(chan[:11], "RyuoBot", msg))
    else:
        console.error("{:<11} - {:<10}: {} - RyuoBot is not allowed to type in {}!".format(chan[:11], "RyuoBot", msg, chan))

def ban(sock, chan, user):
    """
    Ban a user from the current channel.
    Keyword arguments:
    sock -- the socket over which to send the ban commend
    chan -- the channel from which to ban the user
    user -- the user to be banned
    """
    chat(sock, ".ban {}\r\n".format(user))
    console.info("banned user {} from channel {}".format(user, chan))


def timeout(sock, chan, user, secs=600):
    """
    Time out a user for a set period of time.
    Keyword arguments
    sock -- the socket over which to send the timeout command
    chan -- the channel from which to time out the user
    user -- the user to be timed out
    secs -- the length of the timeout in seconds (default 600)
    """
    chat(sock, ".timeout {} {}\r\n".format(user, secs))
    console.info("timed out user {} in channel {} for {} seconds".format(user, chan, secs))
