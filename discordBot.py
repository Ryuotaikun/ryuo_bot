import cfg
import priv
import console
import discordCommands
import sys
import time
import discord
import asyncio
from threading import Thread


class discordbot(Thread):

    def __init__(self, client, daemon=True):
        Thread.__init__(self)
        self.active = True
        self.setName("Discord")
        self.client = client

    def run(self):

        # channels that allow every command

        channels = [
            "debug",
            "spam"
        ]

        # commands that cause an answere

        send_commands = {
            "help": "currently available commands: '!ping', '!ryuobot', '!roll'.\r\nMore will come in the future",
            "ping": "pong",
            "ryuobot": "I am an experimental version of a Twitch/Discord Bot. Read more about me here: <https://www.github.com/Ryuotaikun/ryuo_bot>",
            "turing": "No, I am not self aware but what does it matter as long as we are living in this simulation",
        }

        # commands that cause an elaborate reaction

        function_commands = {
            "game": discordCommands.changeGame,
            "live": discordCommands.announceStream,
            "role": discordCommands.getRoles,
            "off" : discordCommands.logout,
        }

        # commands that cause an elaborate reaction and can be used by every user

        public_function_commands = {
            "roll":  discordCommands.rollDice,
            "hatch": discordCommands.hatch
        }

        @self.client.event
        async def on_ready():
            await self.client.change_presence(game=discord.Game(name="Getting Programmed..."))

        @self.client.event
        async def on_member_join(member):
            print(discord.utils.get(member.server.roles))
            console.info("DISCORD: {} has joined the server".format(member.name))

        @self.client.event
        async def on_message(message):
            console.log("DISCORD: {:<11} - {:<10}: {}".format(str(message.channel)[:11], str(message.author)[:10], str(message.content)))
            if message.content.startswith("!"):
                invoke = message.content[1:].split(" ")[0].lower()
                args = message.content.split(" ")[1:]
                sys.stdout.flush()

                if str(message.author) == "Ryuotaikun#6890" and str(message.channel) == "debug":
                    if invoke in function_commands:
                        await function_commands.get(invoke)(args, message, self.client)

                if str(message.channel) in channels:
                    if invoke in public_function_commands:
                        await public_function_commands.get(invoke)(args, message, self.client)

                if str(message.channel) in channels:
                    if invoke in send_commands:
                        await self.client.send_message(message.channel, send_commands.get(invoke))

                if str(message.author) == "Ryuotaikun#6890" and str(message.channel) == "debug":
                    if invoke == "play":
                        vc = await self.client.join_voice_channel(self.client.get_channel("455429849419350046"))
                        player = await vc.create_ytdl_player(args[0])
                        player.start()

        self.client.run(priv.TOKEN)
