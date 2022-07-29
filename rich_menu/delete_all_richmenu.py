from linebot import LineBotApi, WebhookHandler
from linebot.models import *  # noqa: F401, F403
from config import LINE_API_KEY, WEBHOOK_HANDLER

line_bot_api = LineBotApi(LINE_API_KEY)
handler = WebhookHandler(WEBHOOK_HANDLER)
rich_menu_list = line_bot_api.get_rich_menu_list()
for rich_menu in rich_menu_list:
    print(rich_menu.rich_menu_id)
    line_bot_api.delete_rich_menu(rich_menu.rich_menu_id)
