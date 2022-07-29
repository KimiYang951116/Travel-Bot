from ..config import LINE_API_KEY
from linebot import LineBotApi
from linebot.models import *  # noqa: F401, F403
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
    name='default richmenu',
    chat_bar_text='請完成基本設定',
    areas=[
        RichMenuArea(
            bounds=RichMenuBounds(x=0, y=0, width=2500, height=705),
            action=MessageAction(label='開始', text='開始我的Travel Bot美好體驗')
        ),
        RichMenuArea(
            bounds=RichMenuBounds(x=557, y=705, width=1334, height=692),
            action=MessageAction(label='開始', text='開始我的Travel Bot美好體驗')
        ),
        RichMenuArea(
            bounds=RichMenuBounds(x=0, y=705, width=557, height=692),
            action=URIAction(label='使用條款', uri='https://www.google.com/')
        ),
        RichMenuArea(
            bounds=RichMenuBounds(x=1891, y=705, width=609, height=692),
            action=URIAction(label='個資聲明', uri='https://www.google.com/')
        ),
        RichMenuArea(
            bounds=RichMenuBounds(x=0, y=1397, width=2500, height=289),
            action=URIAction(label='介紹影片', uri='https://www.google.com/')
        )
    ]
)

rich_menu_id = line_bot_api.create_rich_menu(rich_menu=rich_menu_to_create)
print(rich_menu_id)
with open("0.jpg", 'rb') as f:
    line_bot_api.set_rich_menu_image(rich_menu_id, "image/jpeg", f)

line_bot_api.link_rich_menu_to_user('Uc10a26bd60f68b67b4db78d4ee14b8d2', rich_menu_id)  # noqa: E501
