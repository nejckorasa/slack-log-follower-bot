# slack-log-follower-bot

## Synopsis

Simple slack bot that follows file for specific char sequence and notifies you when it appears.

## Motivation

Made for personal use, to follow Maven build log, which takes forever for large projects.

## Configuration

Setting up:

```python
SLACK_BOT_TOKEN = "Your slack bot token"
BOT_ID = "Yout slack bot id"
```

You can find out about how to get bot token and more info at [Slack API page](https://api.slack.com/)

> Note that app must run in same machine as your file you want to follow

## Installation

Simply run **bot.py** after setting configuration as specefied above.

## Usage

In Slack conversation with your bot type:

- "set *file_name* *following_text*"
  - Set a file to follow and text to wait for.
- "start"
  - Start following.
- "follow *file_name* *following_text*"
   - Set a file to follow and text to wait for **and** start following.
- "stop"
   - Stop following.
