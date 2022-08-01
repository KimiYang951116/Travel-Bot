# 3rd party moudule
from linebot import LineBotApi
from linebot.models import *  # noqa: F403, F401
from linebot.models import (
    RichMenu,
    RichMenuArea,
    RichMenuBounds,
    RichMenuSize,
    PostbackAction
)
LINE_API_KEY = '/NWkZeGHgzhXfj6UzLDYIf+xv5n3DHk4zB+YrNB2iIZafn55A44Eqfk3qOZClkK2webGFYYLpf5pQWGXzD0BKAJfJsJm8zDWyNSMnQ6pcgGwtF4j4hHelBnU5kgZUhP0TTiCXJ9fewaSpB+U4RIWawdB04t89/1O/w1cDnyilFU='  # noqa: E501
line_bot_api = LineBotApi(LINE_API_KEY)

rich_menu_to_create = RichMenu(
    size=RichMenuSize(width=2500, height=1686),
    selected=True,
    name='choose_catagory_richmenu',
    chat_bar_text='請選擇查詢地點類別',
    areas=[
        RichMenuArea(
            bounds=RichMenuBounds(x=67, y=69, width=606, height=514),
            action=PostbackAction(label='重選位置', data='/rechoose_location')  # noqa: E501
        ),
        RichMenuArea(
            bounds=RichMenuBounds(x=141, y=1005, width=460, height=534),
            action=PostbackAction(label='查看目前位置', data='/see_location')  # noqa: E501
        ),
        RichMenuArea(
            bounds=RichMenuBounds(x=711, y=169, width=754, height=418),
            action=PostbackAction(label='全部', data='/find/all')
        ),
        RichMenuArea(
            bounds=RichMenuBounds(x=711, y=641, width=754, height=418),
            action=PostbackAction(label='旅館', data='/find/lodging')
        ),
        RichMenuArea(
            bounds=RichMenuBounds(x=711, y=1111, width=754, height=418),
            action=PostbackAction(label='景點', data='/find/tourist_attraction')
        ),
        RichMenuArea(
            bounds=RichMenuBounds(x=1517, y=169, width=754, height=418),
            action=PostbackAction(label='餐廳', data='/find/restaurant')
        ),
        RichMenuArea(
            bounds=RichMenuBounds(x=1517, y=641, width=754, height=418),
            action=PostbackAction(label='加油站', data='/find/gas_station')
        ),
        RichMenuArea(
            bounds=RichMenuBounds(x=1517, y=1111, width=754, height=418),
            action=PostbackAction(label='超商', data='/find/convenience_store')
        ),
    ]
)

rich_menu_id = line_bot_api.create_rich_menu(rich_menu=rich_menu_to_create)
print(rich_menu_id)
with open("2.jpg", 'rb') as f:
    line_bot_api.set_rich_menu_image(rich_menu_id, "image/jpeg", f)

line_bot_api.link_rich_menu_to_user('Uc10a26bd60f68b67b4db78d4ee14b8d2', rich_menu_id)  # noqa: E501
