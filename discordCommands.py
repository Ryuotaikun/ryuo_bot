import time
import random
import discord

mentions = {

}

# list for emote IDs

emotes = {
    "milotic":  "<:milotic:449856384016842774>",
    "snorlax":  "<:snorlax:449868656357277696>",
    "rotom":    "<:rotom:449869028828381197>",
    "magneton": "<:magneton:449868484906844160>",
    "altaria":  "<:altaria:449868760439062529>",
    "absol":    "<:absol:449868948352270346>",
    "gyarados": "<:gyarados:449868569803620355>",
}

# list for role IDs

roles = { # might not be necessary
}

# change the game the bot is playing

async def changeGame(args, message, client):
    newStatus = message.content.partition(" ")[2]
    await client.change_presence(game=discord.Game(name=newStatus))
    await client.send_message(message.channel, embed=discord.Embed(colour=discord.Color.green(), description=("Game has been changed to '{}'".format(newStatus))))

# announce the stream

async def announceStream(args, message, client):
    if len(args) == 0:
        notification_message = "Hey <@&449857211511078913>, Ryuotaikun is now live on Twitch.\r\nCome watch at https://www.twitch.tv/ryuotaikun {}".format(emotes.get("altaria"))
    else:
        notification_message = "Hey <@&449857211511078913>, {}.\r\nCome watch at https://www.twitch.tv/ryuotaikun {}".format(message.content.partition(" ")[2], emotes.get("altaria"))
    await client.send_message(client.get_channel("449245572873060352"), notification_message)

# returns roles in discord (used to learn about granting/taking roles)

async def getRoles(args, message, client):
    await client.send_message(message.channel, "Your current Roles are:")
    roleString = ""
    for role in message.author.roles:
        roleString +=  str(role) + "\n"
    await client.send_message(message.channel, embed=discord.Embed(colour=discord.Color.green(), description=(roleString)))

# closes the connection and ends all discord related threads

async def logout(args, message, client):
    await client.send_message(message.channel, embed=discord.Embed(colour=discord.Color.gold(), description=("RyuoBot goes off")))
    await client.logout()

async def rollDice(args, message, client):
    if len(args) == 0:
        args.append("d100")
    if args[0].startswith("d") or args[0].startswith("D"):
        try:
            limit = int(args[0][1:])
            number = random.randrange(limit) + 1
            await client.send_message(message.channel, "Rolling the Dice...")
            time.sleep(.5)
            await client.send_message(message.channel, embed=discord.Embed(colour=discord.Color.gold(), description=("{} rolled {}".format(message.author.mention, number))))
        except:
            await client.send_message(message.channel, embed=discord.Embed(colour=discord.Color.red(), description=("Please enter a valid argument (d6, d20, d100, etc)")))

async def hatch(arags, message, client):
    if len(message.author.roles) == 1:
        await client.send_message(client.get_channel("449204853408006156"), "A new Hatchling joins the Server. Welcome {} {}".format(message.author.mention, emotes.get("milotic")))
        await client.add_roles(message.author, discord.utils.get(message.author.server.roles, name="Hatchling"))
