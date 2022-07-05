#3rd party module
from linebot.models import ConfirmTemplate, URITemplateAction, URIAction, ButtonComponent, FlexSendMessage, IconComponent, ImageComponent, TextComponent, BoxComponent, BubbleContainer, MessageTemplateAction, CarouselTemplate, CarouselColumn, MessageEvent, TextMessage, LocationMessage, TextSendMessage, QuickReply, QuickReplyButton, MessageAction, ImageSendMessage, StickerSendMessage, LocationSendMessage, TemplateSendMessage

def make_nearby_carousel_template(catagory, column):
    message = TemplateSendMessage(
        alt_text = f'附近的{catagory}',
        template=CarouselTemplate(
        columns=column
    ))
    return message

def make_nearby_carousel_template_column(nearby_place_df):
    column = []
    df_len = len(nearby_place_df.columns)
    if df_len > 9:
        df_len = 9
    for i in range(df_len):
        title = nearby_place_df[i][0]
        if len(title) > 10:
            title = title[:10]
        text = nearby_place_df[i][1]
        if len(text) > 60:
            text = text[:60]
        print(f'{title}\n{text}')
        column.append(CarouselColumn(
            title='搜尋其他項目',
            text = text,
            actions = [
                MessageTemplateAction(
                    label = '返回',
                    text = f'/back'
                )
            ]
        ))
        column.append(CarouselColumn(
            title=title,
            text = text,
            actions = [
                MessageTemplateAction(
                    label = '查看詳細資料',
                    text = f'/detail/{nearby_place_df[i][2]}({nearby_place_df[i][0]})'
                )
            ]
        ))
    return column