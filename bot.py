import random
import threading
import time

from slackclient import SlackClient

import follower

SLACK_BOT_TOKEN = None
BOT_ID = "U2X7SSN9F"
AT_BOT = "<@" + BOT_ID + ">"

slack_client = SlackClient(SLACK_BOT_TOKEN)

start_responses = ["Sure...go get coffee or something", "On it!", "Got it!", "Yes sir!", "Will tell you when it starts"]
stop_responses = ["As ypu wish", "Stopped...!", "Got it, stopped", "Done"]


def start_following(channel):
    follower.server_thread = threading.Thread(target=follower.init_follow, args=(channel,))
    follower.server_thread.start()


def stop_following():
    follower.active = False


def handle_command(command, channel):
    response = "Not sure what you mean!"

    if "start" in command:
        if follower.file_name is None:
            response = "File name not set!"
        elif follower.string is None:
            response = "Follow string not set!"
        else:
            start_following(channel)
            response = start_responses.pop(random.randrange(len(start_responses)))

    if "stop" in command:
        if follower.server_thread is None:
            response = "Not started yet!"
        else:
            stop_following()
            response = stop_responses.pop(random.randrange(len(stop_responses)))

    if "set" in command:
        command_split = command.split(" ")
        follower.file_name = command_split[1]
        follower.string = " ".join(command_split[2:])
        response = "Following " + follower.file_name + "for '" + follower.string + "'"

    if "follow" in command:
        command_split = command.split(" ")
        follower.file_name = command_split[1]
        follower.string = " ".join(command_split[2:])
        start_following(channel)
        response = start_responses.pop(random.randrange(len(start_responses))) + " Following " + follower.file_name + "for '" + follower.string + "'"

    slack_client.api_call("chat.postMessage", channel=channel, text=response, as_user=True)


def parse_output(slack_rtm_output):
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and output["user"] != BOT_ID:
                return output['text'], output['channel']

    return None, None


def post_string_reached(channel):
    slack_client.api_call("chat.postMessage", channel=channel, text="DONE DONE DONE!", as_user=True)


if __name__ == "__main__":

    READ_WEBSOCKET_DELAY = 1
    if slack_client.rtm_connect():
        print("Bot connected and running!")
        while True:
            command, channel = parse_output(slack_client.rtm_read())
            if command and channel:
                handle_command(command, channel)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed!")
