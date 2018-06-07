import discord

async def changeGame(args, message, client):
    newStatus = message.content.partition(" ")[2]
    await client.change_presence(game=discord.Game(name=newStatus))
    await client.send_message(message.channel, message.channel)
    await client.send_message(message.channel, embed=discord.Embed(colour=discord.Color.green(), description=("Game has been changed to '{}'".format(newStatus))))

async def announceStream(args, message, client):
    if len(args) == 0:
        notification_message = "Hey <@&449857211511078913>, Ryuotaikun is now live on Twitch.\r\nCome watch at https://www.twitch.tv/ryuotaikun <:altaria:449868760439062529>"
    else:
        notification_message = "Hey <@&449857211511078913>, {}.\r\nCome watch at https://www.twitch.tv/ryuotaikun <:altaria:449868760439062529>".format(message.content.partition(" ")[2])
    await client.send_message(client.get_channel('449245572873060352'), notification_message)
