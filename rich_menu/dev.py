from linebot import LineBotApi
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

LINE_API_KEY = '/NWkZeGHgzhXfj6UzLDYIf+xv5n3DHk4zB+YrNB2iIZafn55A44Eqfk3qOZClkK2webGFYYLpf5pQWGXzD0BKAJfJsJm8zDWyNSMnQ6pcgGwtF4j4hHelBnU5kgZUhP0TTiCXJ9fewaSpB+U4RIWawdB04t89/1O/w1cDnyilFU='  # noqa: E501
WEBHOOK_HANDLER = 'f28db6c57607c6e4a1b570b8294675cb'


line_bot_api = LineBotApi(LINE_API_KEY)

# with open("menu_1.jpg", 'rb') as f:
#     line_bot_api.set_rich_menu_image("richmenu-8fce423c47c1d11eed9a8074059b0780", "image/jpeg", f)

# line_bot_api.link_rich_menu_to_user('Uc10a26bd60f68b67b4db78d4ee14b8d2', "richmenu-8fce423c47c1d11eed9a8074059b0780")

line_bot_api.set_default_rich_menu("richmenu-8f3bec982eb2b920d60519b5cfbc22a3")

