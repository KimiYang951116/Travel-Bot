from config import LINE_API_KEY
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


line_bot_api.set_default_rich_menu('richmenu-112595219b475989a0b0177473ffa70b')