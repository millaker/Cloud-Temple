import os
from linebot import LineBotApi
from linebot.models import TextSendMessage, ImageSendMessage, TemplateSendMessage, ButtonsTemplate
from linebot.models import ConfirmTemplate, CarouselColumn, CarouselTemplate

access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)
line_bot_api = LineBotApi(access_token)

def send_text_message(reply_token, text):
    line_bot_api.reply_message(reply_token, TextSendMessage(text=text))
    return "OK"

def send_image_url(id, img_url):
    message = ImageSendMessage(
        original_content_url = img_url,
        preview_image_url = img_url
    )
    line_bot_api.reply_message(id, message)

    return "OK"

def push_message(userid, msg):
    line_bot_api.push_message(userid, TextSendMessage(text=msg))

    return "OK"

def send_template_button(id, alt_text, title, text, img_url, actions):
    message = TemplateSendMessage(
        alt_text = alt_text,
        template = ButtonsTemplate(
            thumbnail_image_url = img_url,
            title = title,
            text = text,
            actions = actions
        )
    )
    line_bot_api.reply_message(id, message)

    return "OK"

def send_template_confirm(id, alt_text, text, actions):
    message = TemplateSendMessage(
        alt_text = alt_text,
        template = ConfirmTemplate(
            text = text,
            actions = actions
        )
    )
    line_bot_api.reply_message(id, message)

    return "OK"

def send_template_carousel(id, alt_text, columns):
    message = TemplateSendMessage(
        alt_text = alt_text,
        template = CarouselTemplate(
            columns = columns
        )
    )
    line_bot_api.reply_message(id, message)

    return "OK"

# Check if input is "return"
def is_return(text):
    return text == "return"

# Check if dice roll passed
def is_passed_roll(num):
    return num >= 2