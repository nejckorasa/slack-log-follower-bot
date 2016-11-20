import time
import threading

import bot

stop_event = threading.Event()

server_thread = None
file_name = None
string = None


def init_follow(to_channel):
    stop_event.clear()
    log_file = open(file_name, "r")
    log_lines = follow(log_file)

    for line in log_lines:
        if string in line:
            stop_event.set()
            bot.post_string_reached(to_channel)
            return


def follow(thefile):
    thefile.seek(0, 2)
    while not stop_event.is_set():
        line = thefile.readline()
        if not line:
            time.sleep(0.1)
            continue
        yield line
