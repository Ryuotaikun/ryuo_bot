import cfg
import time
import logging

def chat(sock, msg):
    """
    Send a chat message to the server.
    Keyword arguments:
    sock -- the socket over which to send the message
    msg  -- the message to be send
    """
    sock.send("PRIVMSG {} :{}\r\n".format(cfg.CHAN, msg).encode())
    logging.info("RyuoBot: {}".format(msg))

def ban(sock, user):
    """
    Ban a user from the current channel.
    Keyword arguments:
    sock -- the socket over which to send the ban commend
    user -- the user to be banned
    """
    chat(sock, ".ban {}\r\n".format(user))
    logging.info("banned user {} from channel {}".format(user, cfg.CHAN))


def timeout(sock, user, secs=600):
    """
    Time out a user for a set period of time.
    Keyword arguments
    sock -- the socket over which to send the timeout command
    user -- the user to be timed out
    secs -- the length of the timeout in seconds (default 600)
    """
    chat(sock, ".timeout {} {}\r\n".format(user, secs))
    logging.info("timed out user {} for {} seconds".format(user, secs))
