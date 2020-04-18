from slackeventsapi import SlackEventAdapter
from slack import WebClient
import json
import os
import ssl as ssl_lib
import certifi
import logging


tokens = {}
with open('configs.json') as json_data:
    tokens = json.load(json_data)

app = Flask(__name__)
slack_events_adapter = SlackEventAdapter(tokens.get("slack_signing_secret"), "/slack/events", app)
slack_web_client = WebClient(tokens.get("slack_bot_token"))


@slack_events_adapter.on("message")
def handle_message(event_data):
    message = event_data["event"]
    if message.get("subtype") is None and "BOT TEST" in message.get('text'):
        channel = message["channel"]
        user = message["user"]
        send_message = f'Thanks for chatting with me, <@{user}>! If you can, give me a :heart:'
        slack_web_client.chat_postMessage(channel=channel, text=send_message)


@slack_events_adapter.on("error")
def error_handler(err):
    print("ERROR: " + str(err))


if __name__ == '__main__':
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler())
    ssl_context = ssl_lib.create_default_context(cafile=certifi.where())
    app.run(port=3000)