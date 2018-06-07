import sys
import priv
import console
import discordCommands
import discord
import asyncio
from threading import Thread


class discordbot(Thread):

    def __init__(self):
        Thread.__init__(self)
        self.active = True

    def run(self):

        client = discord.Client(loop=asyncio.new_event_loop())

        send_commands = {
            "ping": "pong",
        }

        function_commands = {
            "game": discordCommands.changeGame,
            "live": discordCommands.announceStream,
        }

        @client.event
        async def on_ready():
            await client.change_presence(game=discord.Game(name="Getting Programmed..."))

        @client.event
        async def on_message(message):
            console.log("DISCORD: {:<11} - {:<10}: {}".format(str(message.channel)[:11], str(message.author)[:10], str(message.content)))
            if message.content.startswith("!"):
                invoke = message.content[1:].split(" ")[0]
                args = message.content.split(" ")[1:]
                sys.stdout.flush()
                if str(message.author) == "Ryuotaikun#6890":
                    if invoke in function_commands:
                        await function_commands.get(invoke)(args, message, client)

                if invoke in send_commands:
                    await client.send_message(message.channel, send_commands.get(invoke))

        client.run(priv.TOKEN)
