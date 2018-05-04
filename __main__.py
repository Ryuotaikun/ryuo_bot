# twitchbot RyuoBot

# Developed by Ryuotaikun
# With Help from iamflemming

# __main__.py
import cfg
import multi
import console

def main():

    console.info("RyuoBot running...")

    multi.chatbot(cfg.CHAN).start()

main()
