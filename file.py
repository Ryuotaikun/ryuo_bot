import twitch
import console
import yaml

CHAN_FILE_PATH = r"D:\Users\Ryuotaikun\Documents\programming\Python\RyuoBot\ryuo_bot\channels.yaml"

"""
restore is called when the program starts to reconnect to all channels with
the right settings
"""
def restore():
    with open(CHAN_FILE_PATH) as file:
        active_channels = yaml.load(file)

    for entry in active_channels:
        twitch.twitchbot(entry["channel"], entry["status"]).start()

"""
addChannel/removeChannel adds/removes the specified channel to/from the yaml file
"""
def addChannel(chan):
    with open(CHAN_FILE_PATH) as file:
        active_channels = yaml.load(file)

    active_channels.append({"channel": chan, "status" : "lurking"})

    with open(CHAN_FILE_PATH, "w") as file:
        yaml.dump(active_channels, file, default_flow_style = False)

def removeChannel(chan):
    with open(CHAN_FILE_PATH) as file:
        active_channels = yaml.load(file)

    for entry in active_channels:
        if entry["channel"] == chan:
            active_channels.remove(entry)
            break

    with open(CHAN_FILE_PATH, "w") as file:
        yaml.dump(active_channels, file, default_flow_style = False)

"""
updateState changes the state of a channel in the yaml file to lurking, active
or verified
"""
def updateStatus(chan, mode):
    with open(CHAN_FILE_PATH) as file:
        active_channels = yaml.load(file)

    for entry in active_channels:
        if entry["channel"] == chan:
            entry["status"] = mode
            break
    else:
        console.error("{:<24}: RyuoBot is not connected to {}!".format(chan[:24], chan))

    print(twitch.twitchbot(chan, mode))

    with open(CHAN_FILE_PATH, "w") as file:
        yaml.dump(active_channels, file, default_flow_style = False)

    if mode == "lurking":
        console.info("{:<24}: RyuoBot is no longer allowed to type in {}!".format(chan[:24], chan))

    elif mode == "active":
        console.info("{:<24}: RyuoBot is now allowed to type in {}!".format(chan[:24], chan))

    elif mode == "verified":
        console.info("{:<24}: RyuoBot is now verified in {}!".format(chan[:24], chan))
