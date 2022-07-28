from linebot import LineBotApi
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    ConfirmTemplate,
    URITemplateAction,
    URIAction,
    ButtonComponent,
    FlexSendMessage,
    IconComponent,
    ImageComponent,
    TextComponent,
    BoxComponent,
    BubbleContainer,
    MessageTemplateAction,
    CarouselTemplate,
    CarouselColumn,
    MessageEvent,
    TextMessage,
    LocationMessage,
    TextSendMessage,
    QuickReply,
    QuickReplyButton,
    MessageAction,
    ImageSendMessage,
    StickerSendMessage,
    LocationSendMessage,
    TemplateSendMessage,
    RichMenuSize,
    RichMenu,
    RichMenuArea,
    RichMenuBounds
)
from config import LINE_API_KEY, WEBHOOK_HANDLER

line_bot_api = LineBotApi(LINE_API_KEY)
handler = WebhookHandler(WEBHOOK_HANDLER)
rich_menu_list = line_bot_api.get_rich_menu_list()
for rich_menu in rich_menu_list:
    print(rich_menu.rich_menu_id)