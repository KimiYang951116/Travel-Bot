# 3rd party module
from flask import Flask, request, abort
import pandas as pd
import pymysql

# Line bot module
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    ConfirmTemplate,
    FlexSendMessage,
    MessageEvent,
    TextMessage,
    LocationMessage,
    TextSendMessage,
    TemplateSendMessage,
    PostbackEvent,
    LocationSendMessage,
    MessageTemplateAction
)
from linebot.models import *  # noqa: F401, F403


# My module
from functions.sql import AddUserInfo, CheckUserExistance, GetUserInfo, UpdateUserInfo  # noqa: E501
from functions.find_places import find_nearby_places, find_place_details
from functions.line_sdk import (
    make_general_bubble_component,
    make_place_bubble_component,
    make_nearby_carousel_template,
    make_nearby_carousel_template_column,
)
from config import (
    LINE_API_KEY,
    RANKBY_DICT,
    WEBHOOK_HANDLER,
    no_location_richmenu_id,
    default_richmenu_id,
    choose_catagory_richmenu_id,
    is_agreeTrue,
    is_agreeFalse
)


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
def handle_text_message(event):
    user_id = event.source.user_id
    connection = pymysql.connect(
        host="us-cdbr-east-05.cleardb.net",
        user="b5f2e205874506",
        password="3291697e",
        db="heroku_b2cccf87a825db4",
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    etext = event.message.text
    try:
        user_rich = line_bot_api.get_rich_menu_id_of_user(user_id)
    except Exception:
        line_bot_api.link_rich_menu_to_user(user_id, default_richmenu_id)
        user_rich = default_richmenu_id
    multimessage = []
    is_exist = CheckUserExistance(connection, user_id)
    if not is_exist:
        AddUserInfo(connection, user_id)
    if etext == '開始我的Travel Bot美好體驗':
        is_agree = GetUserInfo(connection, user_id, 'service')
        if is_agree == 0:
            multimessage.append(TextSendMessage(text="歡迎使用Travel Bot"))
            multimessage.append(TextSendMessage(text="你尚未同意我們的個人資料告知事項及同意事項以及使用條款(以下簡稱事項及條款)，請先同意我們的事項及條款。完整事項及條款可至下方選單連結查看"))  # noqa: E501
            multimessage.append(TemplateSendMessage(
                alt_text='同意我們的同意事項?',
                template=ConfirmTemplate(
                    text='你是否同意我們的同意事項?',
                    actions=[
                        MessageTemplateAction(
                            label='我同意',
                            text='/service/1'
                        ),
                        MessageTemplateAction(
                            label='我不同意',
                            text='/service/0'
                        )
                    ]
                )
            ))
        else:
            bubble = make_general_bubble_component('你已經完成基本設定了')
            multimessage.append(FlexSendMessage(alt_text='你已經完成基本設定了', contents=bubble))
            if user_rich != no_location_richmenu_id and user_rich != choose_catagory_richmenu_id:  # noqa: E501
                line_bot_api.link_rich_menu_to_user(user_id, no_location_richmenu_id)  # noqa: E501
    elif etext.startswith('/service'):
        is_agree = GetUserInfo(connection, user_id, 'service')
        if is_agree == 0:
            proetext = etext.split('/')
            proetext = proetext[2]
            if proetext == '1':
                UpdateUserInfo(connection, user_id, 'service', 1)
                bubble = make_general_bubble_component(is_agreeTrue)
                multimessage.append(FlexSendMessage(alt_text=is_agreeTrue, contents=bubble))  # noqa: E501
                line_bot_api.link_rich_menu_to_user(user_id, no_location_richmenu_id)  # noqa: E501
            else:
                bubble = make_general_bubble_component(is_agreeFalse)
                multimessage.append(FlexSendMessage(alt_text=is_agreeFalse, contents=bubble))  # noqa: E501
        else:
            multimessage.append(TextSendMessage(text='你已經完成基本設定了'))
            line_bot_api.link_rich_menu_to_user(user_id, no_location_richmenu_id)  # noqa: E501
    if etext == '測試':
        multimessage.append(TextSendMessage(text=user_id))
    if len(multimessage) > 0 and len(multimessage) < 6:
        line_bot_api.reply_message(event.reply_token, multimessage)


@handler.add(MessageEvent, message=LocationMessage)
def handle_location_message(event):
    connection = pymysql.connect(
        host="us-cdbr-east-05.cleardb.net",
        user="b5f2e205874506",
        password="3291697e",
        db="heroku_b2cccf87a825db4",
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    user_id = event.source.user_id
    is_exist = CheckUserExistance(connection, user_id)
    try:
        user_rich = line_bot_api.get_rich_menu_id_of_user(user_id)
    except Exception:
        line_bot_api.link_rich_menu_to_user(user_id, default_richmenu_id)
        user_rich = default_richmenu_id
    multimessage = []
    if not is_exist:
        if user_rich != default_richmenu_id:
            line_bot_api.link_rich_menu_to_user(user_id, default_richmenu_id)
        bubble = make_general_bubble_component('請先完成基本設定')
        multimessage.append(FlexSendMessage(alt_text='請先完成基本設定', contents=bubble))
    else:
        is_agree = GetUserInfo(connection, user_id, 'service')
        if is_agree == 0:
            if user_rich != default_richmenu_id:
                line_bot_api.link_rich_menu_to_user(user_id, default_richmenu_id)  # noqa: E501
            bubble = make_general_bubble_component('請先完成基本設定')
            multimessage.append(FlexSendMessage(alt_text='請先完成基本設定', contents=bubble))
        else:
            latitude = event.message.latitude
            longitude = event.message.longitude
            latlong = f'{latitude},{longitude}'
            UpdateUserInfo(connection, user_id, 'latlong', latlong)
            line_bot_api.link_rich_menu_to_user(user_id, choose_catagory_richmenu_id)    # noqa: E501
    if len(multimessage) > 0 and len(multimessage) < 6:
        line_bot_api.reply_message(event.reply_token, multimessage)


@handler.add(PostbackEvent)
def handle_postback_message(event):
    connection = pymysql.connect(
        host="us-cdbr-east-05.cleardb.net",
        user="b5f2e205874506",
        password="3291697e",
        db="heroku_b2cccf87a825db4",
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    user_id = event.source.user_id
    edata = event.postback.data
    multimessage = []
    is_exist = CheckUserExistance(connection, user_id)
    try:
        user_rich = line_bot_api.get_rich_menu_id_of_user(user_id)
    except Exception:
        line_bot_api.link_rich_menu_to_user(default_richmenu_id)
        user_rich = default_richmenu_id
    if not is_exist:
        bubble = make_general_bubble_component('請先完成基本設定')
        multimessage.append(FlexSendMessage(alt_text='請先完成基本設定', contents=bubble))
        if user_rich != default_richmenu_id:
            line_bot_api.link_rich_menu_to_user(user_id, default_richmenu_id)
    else:
        is_agree = GetUserInfo(connection, user_id, 'service')
        if is_agree == 0:
            if user_rich != default_richmenu_id:
                line_bot_api.link_rich_menu_to_user(user_id, default_richmenu_id)  # noqa: E501
            bubble = make_general_bubble_component('請先完成基本設定')
            multimessage.append(FlexSendMessage(alt_text='請先完成基本設定', contents=bubble))
        else:
            latlong = GetUserInfo(connection, user_id, 'latlong')
            if latlong != 'None':
                if edata.startswith('/find'):
                    print('yes')
                    proetext = edata.split('/')
                    proetext = proetext[2]
                    nearby_places = find_nearby_places(catagory=proetext, rankby=RANKBY_DICT[proetext], latlong=latlong)  # noqa: E501
                    print(nearby_places)
                    if type(nearby_places) == pd.core.frame.DataFrame:
                        columns = make_nearby_carousel_template_column(nearby_places, latlong)  # noqa: E501
                        if columns != 'ERROR_OCCURED':
                            multimessage.append(make_nearby_carousel_template(proetext, columns))  # noqa: E501
                        else:
                            multimessage.append(TextSendMessage(text='發生錯誤'))
                elif edata.startswith('/detail'):
                    information = edata.split('/')[2]
                    placeID = information.split('(')[0]
                    place_name = information.split('(')[1].split(')')[0]
                    detail = find_place_details(placeID)
                    bubble = make_place_bubble_component(place_name, detail, latlong)
                    multimessage.append(FlexSendMessage(alt_text='彈性配置', contents=bubble))  # noqa: E501
                elif edata == '/see_location':
                    latitude = latlong.split(',')[0]
                    longitude = latlong.split(',')[1]
                    multimessage.append(LocationSendMessage(title='你的位置', address='你向Travel Bot所提供的位置', latitude=latitude, longitude=longitude))    # noqa: E501
                elif edata == '/rechoose_location':
                    line_bot_api.link_rich_menu_to_user(user_id, no_location_richmenu_id)  # noqa: E501
            else:
                bubble = make_general_bubble_component('你尚未提供你的位置')
                multimessage.append(FlexSendMessage(alt_text='你尚未提供你的位置', contents=bubble))
                if user_rich != no_location_richmenu_id:
                    line_bot_api.link_rich_menu_to_user(user_id, no_location_richmenu_id)  # noqa: E501
    if len(multimessage) > 0 and len(multimessage) < 6:
        line_bot_api.reply_message(event.reply_token, multimessage)


if __name__ == '__main__':
    app.run()
