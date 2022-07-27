# 3rd party module
from linebot.models import (
    MessageTemplateAction,
    CarouselTemplate,
    CarouselColumn,
    QuickReplyButton,
    MessageAction,
    TemplateSendMessage,
    PostbackAction,
    BubbleContainer,
    BoxComponent,
    TextComponent,
    ImageComponent,
    IconComponent,
    ButtonComponent,
    URIAction
)

def make_nearby_carousel_template(catagory, column):
    '''
    The function takes the list returned by make_nearby_carousel_template_column as
    an input and outputs the TemplateSendMessage
    it uses linebot sdk module, for more details, see
    https://developers.line.biz/en/docs/messaging-api

    parameters:
    1. catagory : the catatory of places you want to find nearby
    2. column : a list that is returned by the function make_nearby_carousel_template_column

    return values:
    1. normal : returns a variable that can be used in sending linebot messages
    2. error : returns 'ERROR_OCCURED'
    '''
    try:
        message = TemplateSendMessage(
            alt_text=f'附近的{catagory}',
            template=CarouselTemplate(columns=column)
        )
        return message
    except Exception:
        return 'ERROR_OCCURED'


def make_nearby_carousel_template_column(nearby_place_df):
    '''
    The function takes a dataframe returned by find_nearby_places and outputs a list of
    CarouselColumns
    it uses linebot sdk module, for more details, see
    https://developers.line.biz/en/docs/messaging-api
    parameters:
    1. nearby_place_df : a pandas dataframe returned by the find_nearby_places function

    return values:
    1. normal : returns a list that contains CarouselColumns that can be used as a input in the
    make_nearby_carousel_template_column
    2. error : returns 'ERROR_OCCURED'
    '''
    try:
        column = []
        df_len = len(nearby_place_df.columns)
        if df_len > 9:
            df_len = 9
        column.append(CarouselColumn(
            title='搜尋其他項目',
            text='回到前頁',
            actions=[
                MessageTemplateAction(
                    label='返回',
                    text='/back'
                )
            ]
        ))
        for i in range(df_len):
            title = nearby_place_df[i][0]
            if len(title) > 10:
                title = title[:10]
            text = nearby_place_df[i][1]
            if len(text) > 60:
                text = text[:60]
            print(f'{title}\n{text}')
            column.append(CarouselColumn(
                title=title,
                text=text,
                actions=[
                    MessageTemplateAction(
                        label='查看詳細資料',
                        text=f'/detail/{nearby_place_df[i][2]}({nearby_place_df[i][0]})'
                    )
                ]
            ))
        return column
    except Exception:
        return 'ERROR_OCCURED'


def make_quick_reply_item_lst(label_lst, text_lst):
    quick_reply_lst = []
    if len(label_lst) == len(text_lst):
        try:
            for i in range(len(label_lst)):
                quick_reply_lst.append(QuickReplyButton(action=PostbackAction(label=label_lst[i], data=text_lst[i])))
            return quick_reply_lst
        except Exception:
            return 'ERROR_OCCURED'
    else:
        return 'ERROR_OCCURED'


def make_bubble_component(place_name, detail_lst):
    openhr, address, phone, rate, price = detail_lst[0], detail_lst[1], detail_lst[2], detail_lst[3], detail_lst[4]
    bubble = BubbleContainer(
        direction = 'ltr',
        header = BoxComponent(
            layout = 'vertical',
            contents = [
                TextComponent(
                    text = place_name,
                    weight = 'bold',
                    size = 'xxl'
                ),
            ]
        ),
        body = BoxComponent(
            layout = 'vertical',
            contents = [
                BoxComponent(
                    layout = 'baseline',
                    contents = [
                        IconComponent(
                            url = 'https://cdn-icons-png.flaticon.com/512/217/217887.png',
                            size = 'lg'
                        ),
                        TextComponent(
                            text = f'  {phone}',
                            size = 'lg'
                        )
                    ]
                ),
                BoxComponent(
                    layout = 'baseline',
                    contents = [
                        IconComponent(
                            url = 'https://cdn-icons-png.flaticon.com/512/235/235861.png',
                            size = 'lg'
                        ),
                        TextComponent(
                            text = f'  {address}',
                            size = 'md'
                        )
                    ]
                ),
                BoxComponent(
                    layout = 'baseline',
                    contents = [
                        IconComponent(
                            url = 'https://img.tukuppt.com/ad_preview/00/31/67/ObvzW3N3kV.jpg!/both/260x260',
                            size = 'lg'
                        ),
                        TextComponent(
                            text = f'  {openhr}',
                            size = 'md'
                        )
                    ]
                ),
                BoxComponent(
                    layout = 'baseline',
                    contents = [
                        IconComponent(
                            url = 'https://cdn-icons-png.flaticon.com/512/3629/3629625.png', 
                            size = 'lg'
                        ),
                        TextComponent(
                            text = f'  {rate}',
                            size = 'md'
                        ),
                        IconComponent(
                            url = 'https://cdn-icons-png.flaticon.com/512/189/189715.png', 
                            size = 'lg'
                        ),
                        TextComponent(
                            text = f'  {price}',
                            size = 'md'
                        ),
                    ]
                ),
                BoxComponent(
                    layout = 'horizontal',
                    margin = 'xxl',
                    contents = [
                        ButtonComponent(
                            style = 'primary',
                            height = 'sm',
                            action = URIAction(label ='電話聯絡', uri = f'tel:{phone}'),
                        ),
                        ButtonComponent(
                            style = 'secondary',
                            height = 'sm',
                            action = PostbackAction(label='測試用', data='hihi')
                        )
                    ]
                )
        
            ]
        ),
    )
    return bubble
