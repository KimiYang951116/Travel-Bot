# 3rd party module
from flask import Flask, request, abort
import requests
import time
import pymysql

# Line bot module
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import ConfirmTemplate, URITemplateAction, URIAction, ButtonComponent, FlexSendMessage, IconComponent, ImageComponent, TextComponent, BoxComponent, BubbleContainer, MessageTemplateAction, CarouselTemplate, CarouselColumn, MessageEvent, TextMessage, LocationMessage, TextSendMessage, QuickReply, QuickReplyButton, MessageAction, ImageSendMessage, StickerSendMessage, LocationSendMessage, TemplateSendMessage

# My module
from sql import AddUserInfo, CheckUserExistance, GetUserInfo
from config import LINE_API_KEY, WEBHOOK_HANDLER, RULES
from find_places import find_restaurant

line_bot_api = LineBotApi(LINE_API_KEY)
handler = WebhookHandler(WEBHOOK_HANDLER)
app = Flask(__name__)


@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'ok'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    etext = event.message.text
    

        
@handler.add(MessageEvent, message=LocationMessage)
def handle_message(event):
    connection = pymysql.connect(
        host="us-cdbr-east-05.cleardb.net",
        user="b5f2e205874506",
        password="3291697e",
        db="heroku_b2cccf87a825db4",
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    user_id = event.source.user_id
    user_name = line_bot_api.get_profile(user_id)
    multimessage = []
    is_exist = CheckUserExistance(connection, user_id)
    if is_exist == False:
        multimessage.append(TextSendMessage(text=f'你目前不再資料庫中，現在將立即為你新增'))
        AddUserInfo(connection, user_id)
        multimessage.append(TextSendMessage(text=f'已經成功將你加入資料庫\n歡迎你{user_name.display_name}，接著請同意我們的使用條款'))
    is_agree = GetUserInfo(connection, user_id, 'service')
    if is_agree == 0:
        multimessage.append(TextSendMessage(text="你尚未同意我們的使用條款，請先同意我們的條款\n"\
        "條款網址如下"))
        multimessage.append(TextSendMessage(text=RULES))
        multimessage.append(TemplateSendMessage(
            alt_text = '同意使用條款?',
            template = ConfirmTemplate(
                text = '你是否同意我們的使用條款?',
                actions = [
                    MessageTemplateAction(
                        label = '我同意',
                        text = '/service/yes'
                    ),
                    MessageTemplateAction(
                        label = '我不同意',
                        text = '/service/no'
                    )
                ]
            )
        ))
    else:
        multimessage.append(TextSendMessage(text = 'hi'))
    line_bot_api.reply_message(event.reply_token, multimessage)
