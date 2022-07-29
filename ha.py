from config import LINE_API_KEY, default_richmenu_id
from linebot import LineBotApi
from linebot.models import *
line_bot_api = LineBotApi(LINE_API_KEY)
line_bot_api.link_rich_menu_to_user('Uc10a26bd60f68b67b4db78d4ee14b8d2', default_richmenu_id)