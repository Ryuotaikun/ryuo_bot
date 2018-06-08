import discord

mentions = {

}

emotes = {
    "milotic":  "<:milotic:449856384016842774>",
    "snorlax":  "<:snorlax:449868656357277696>",
    "rotom":    "<:rotom:449869028828381197>",
    "magneton": "<:magneton:449868484906844160>",
    "altaria":  "<:altaria:449868760439062529>",
    "absol":    "<:absol:449868948352270346>",
    "gyarados": "<:gyarados:449868569803620355>",
}

async def changeGame(args, message, client):
    newStatus = message.content.partition(" ")[2]
    await client.change_presence(game=discord.Game(name=newStatus))
    await client.send_message(message.channel, embed=discord.Embed(colour=discord.Color.green(), description=("Game has been changed to '{}'".format(newStatus))))

async def announceStream(args, message, client):
    if len(args) == 0:
        notification_message = "Hey <@&449857211511078913>, Ryuotaikun is now live on Twitch.\r\nCome watch at https://www.twitch.tv/ryuotaikun {}".format(emotes.get("altaria"))
    else:
        notification_message = "Hey <@&449857211511078913>, {}.\r\nCome watch at https://www.twitch.tv/ryuotaikun {}".format(message.content.partition(" ")[2], emotes.get("altaria"))
    await client.send_message(client.get_channel('449245572873060352'), notification_message)

async def getRoles(args, message, client):
    #await client.send_message(message.channel, "Your current Roles are:")
    #roleString = ""
    #for role in message.author.roles:
    #    roleString +=  str(role) + "\n"
    #await client.send_message(message.channel, embed=discord.Embed(colour=discord.Color.green(), description=(roleString)))
    role = discord.utils.get(discord.Server.roles, name="Hatchling")
    print(role)
    #await client.add_roles(message.author, role)
