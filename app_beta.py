# 3rd party module
from flask import Flask, request, abort
import requests
import time
import pymysql
import pandas as pd

# Line bot module
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import ConfirmTemplate, URITemplateAction, URIAction, ButtonComponent, FlexSendMessage, IconComponent, ImageComponent, TextComponent, BoxComponent, BubbleContainer, MessageTemplateAction, CarouselTemplate, CarouselColumn, MessageEvent, TextMessage, LocationMessage, TextSendMessage, QuickReply, QuickReplyButton, MessageAction, ImageSendMessage, StickerSendMessage, LocationSendMessage, TemplateSendMessage

# My module
from functions.sql import AddUserInfo, CheckUserExistance, GetUserInfo, UpdateUserInfo
from functions.find_places import find_nearby_places
from functions.line_sdk import make_nearby_carousel_template, make_nearby_carousel_template_column
from config import LINE_API_KEY, RANKBY_DICT, WEBHOOK_HANDLER, RULES

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
    connection = pymysql.connect(
        host="us-cdbr-east-05.cleardb.net",
        user="b5f2e205874506",
        password="3291697e",
        db="heroku_b2cccf87a825db4",
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    etext = event.message.text
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
        if etext.startswith('/service'):
            proetext = etext.split('/')
            proetext = proetext[2]
            if proetext == '1':
                UpdateUserInfo(connection, user_id, 'service', 1)
                multimessage.append(TextSendMessage(text = 'OK，你現在可以開始使用Travel Bot 的所有功能'))
            else:
                multimessage.append(TextSendMessage(text = '很抱歉，由於你不同意我們的同意事項，我們無法為你提供服務，同意我們的同意事項以獲得服務'))
        else:
            multimessage.append(TextSendMessage(text="你尚未同意我們的個人資料告知事項及同意事項(以下簡稱同意事項)，請先同意我們的同意事項\n"\
            "條款如下"))
            multimessage.append(TextSendMessage(text=RULES))
            multimessage.append(TemplateSendMessage(
                alt_text = '同意我們的同意事項?',
                template = ConfirmTemplate(
                    text = '你是否同意我們的同意事項?',
                    actions = [
                        MessageTemplateAction(
                            label = '我同意',
                            text = '/service/1'
                        ),
                        MessageTemplateAction(
                            label = '我不同意',
                            text = '/service/0'
                        )
                    ]
                )
            ))
    if etext.startswith('/find'):
        proetext = etext.split('/')
        proetext = proetext[2]
        latlong = GetUserInfo(connection, user_id, 'latlong')
        nearby_places = find_nearby_places(catagory=proetext[2], rankby = RANKBY_DICT[proetext[2]], latlong = latlong)
        if type(nearby_places) == pd.core.frame.DataFrame:
            columns = make_nearby_carousel_template_column(nearby_places)
            multimessage.append = make_nearby_carousel_template(proetext[2], columns)
    if len(multimessage) > 0 and len(multimessage) < 6:
        line_bot_api.reply_message(event.reply_token, multimessage)

    

        
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
                        text = '/service/1'
                    ),
                    MessageTemplateAction(
                        label = '我不同意',
                        text = '/service/0'
                    )
                ]
            )
        ))
    else:
        latitude = event.message.latitude
        longitude = event.message.longitude
        latlong = f'{latitude},{longitude}'
        UpdateUserInfo(connection, user_id, 'latlong', latlong)
        multimessage.append(TextSendMessage(
            text = '請問你要搜尋附近的甚麼項目?',
            quick_reply = QuickReply(
                items=[
                    QuickReplyButton(
                        action=MessageAction(label='全部', text='/find')
                    ),
                    QuickReplyButton(
                        action=MessageAction(label='餐廳', text='/find/restaurant')
                    ),
                    QuickReplyButton(
                        action=MessageAction(label='加油站', text='/find/gas_station')
                    ),
                    QuickReplyButton(
                        action=MessageAction(label='旅館', text='/find/lodging')
                    ),
                    QuickReplyButton(
                        action=MessageAction(label='景點', text='/find/tourist_attraction')
                    ),
                    QuickReplyButton(
                        action=MessageAction(label='便利商店', text='/find/convenience_store')
                    ),
                ]
            )
        ))
    line_bot_api.reply_message(event.reply_token, multimessage)

        
