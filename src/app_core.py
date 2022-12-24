import os

from flask import Flask, request, abort
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

from utils import send_image_url, send_text_message, is_return, is_passed_roll
from machine import create_machine

app = Flask(__name__, static_folder = "assets")

# Get channel_secret and channel_access_token from environment variable
channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)
channel_secret = os.getenv("LINE_CHANNEL_SECRET", None)

line_bot_api = LineBotApi(channel_access_token)
parser = WebhookParser(channel_secret)

# Unique FSM for each user
machines = {}

@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue
        if not isinstance(event.message.text, str):
            continue
    
        # Create a machine for new user
        if event.source.user_id not in machines:
            machines[event.source.user_id] = create_machine()

        curr_machine = machines[event.source.user_id]
        #Advance the FSM for each MessageEvent
        response = curr_machine.advance(event)
        if response == False:
            if is_return(event.message.text):
                curr_machine.go_Main(event)
            elif ((curr_machine.state == "DiceOne" or 
                  curr_machine.state == "DiceTwo" or
                  curr_machine.state == "Start") and 
                  not is_passed_roll(curr_machine.diceroll)):
                curr_machine.go_Fail(event)
            else:
                send_text_message(event.reply_token, "Wrong input, try again")

    return "OK"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)