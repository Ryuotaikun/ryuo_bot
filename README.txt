Basic Twitch Bot able to moderate a channel and interact with users

Functions include:
- Tracking chat history
- Timing out links and banned words
- Reacting to custom commands (still hardcoded)
- Reacting to subscriptions

NOTE:
At all times, if the bot is going rouge it can be removed from a channel by
typing "!ryuo exit" in the chat. This command is only available to the
moderators and the owner of a channel.

Set Up:
- Create a new folder <fol_name> for the bot and copy the files in
- Create a Twitch account for the bot or use your own account
- Generate an OAuth Token (https://twitchapps.com/tmi/)
- Create a file priv.py with
  NICK = <account name> #lowercase
  PASS = <oauth token>
- Run the program in the terminal with
  'python <fol_name> <twitch_channel>'
  or
  'python3 <fol_name> <twitch_channel>'

You need python3 to run this program
I am not responsible for any problems with the twitch guidelines or other rules
if you run and/or edit this bot.
