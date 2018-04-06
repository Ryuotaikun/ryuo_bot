Basic Twitch Bot able to moderate a channel and interact with users

Functions include:
- Tracking chat history
- Timing out links and banned words
- Reacting to custom commands (still hardcoded)

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
