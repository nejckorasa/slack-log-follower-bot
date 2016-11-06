import time

import bot

active = True
server_thread = None
file_name = None
string = None
channel = None

def init_follow(to_channel):
    global started
    global active
    global channel
    channel = to_channel
    active = True
    log_file = open(file_name, "r")
    log_lines = follow(log_file)
    for line in log_lines:
        if string in line:
            active = False
            bot.post_string_reached(channel)
            return



def follow(thefile):
    thefile.seek(0, 2)
    while active is True:
        line = thefile.readline()
        if not line:
            time.sleep(0.1)
            continue
        yield line
