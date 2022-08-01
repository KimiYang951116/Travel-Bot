from config import LINE_API_KEY
from linebot import LineBotApi
from linebot.models import *  # noqa: F403, F401
from linebot.models import (
    RichMenu,
    RichMenuArea,
    RichMenuBounds,
    RichMenuSize,
    MessageAction,
    URIAction
)

line_bot_api = LineBotApi(LINE_API_KEY)

rich_menu_to_create = RichMenu(
    size=RichMenuSize(width=2500, height=1686),
    selected=True,
    name='no location richmenu',
    chat_bar_text='請提供你的位置資訊',
    areas=[
        RichMenuArea(
            bounds=RichMenuBounds(x=0, y=0, width=2500, height=937),
            action=MessageAction(label='說明', text='你目前尚未向我們提供你的位置資訊，故我們無法進行地點搜尋，有關如何分享位置，請點選下方選單"如何提供"按鈕。如已經分享卻仍顯示此畫面，請重新分享，或稍待片刻')  # noqa: E501
        ),
        RichMenuArea(
            bounds=RichMenuBounds(x=0, y=937, width=1949, height=749),
            action=MessageAction(label='說明', text='你目前尚未向我們提供你的位置資訊，故我們無法進行地點搜尋，有關如何分享位置，請點選下方選單"如何提供"按鈕。如已經分享卻仍顯示此畫面，請重新分享，或稍待片刻')  # noqa: E501
        ),
        RichMenuArea(
            bounds=RichMenuBounds(x=1949, y=937, width=551, height=749),
            action=URIAction(label='如何提供', uri='https://www.google.com/')
        ),
    ]
)

rich_menu_id = line_bot_api.create_rich_menu(rich_menu=rich_menu_to_create)
print(rich_menu_id)
with open("1.jpg", 'rb') as f:
    line_bot_api.set_rich_menu_image(rich_menu_id, "image/jpeg", f)

line_bot_api.link_rich_menu_to_user('Uc10a26bd60f68b67b4db78d4ee14b8d2', rich_menu_id)  # noqa: E501
