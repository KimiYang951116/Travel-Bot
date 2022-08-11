# 3rd party module
from linebot.models import *  # noqa: F403, F401
from linebot.models import (
    TemplateSendMessage,
    CarouselTemplate,
    CarouselColumn,
    PostbackTemplateAction,
    QuickReplyButton,
    PostbackAction,
    BubbleContainer,
    TextComponent,
    IconComponent,
    BoxComponent,
    ButtonComponent,
    URIAction,
    ImageComponent
)

from functions.find_places import calculate_distance, generate_guild_link


def make_nearby_carousel_template(catagory, column):
    '''
    The function takes the list returned by
    make_nearby_carousel_template_column as
    an input and outputs the TemplateSendMessage
    it uses linebot sdk module, for more details, see
    https://developers.line.biz/en/docs/messaging-api

    parameters:
    1. catagory : the catatory of places you want to find nearby
    2. column : a list that is returned by the function
    make_nearby_carousel_template_column

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


def make_nearby_carousel_template_column(nearby_place_df, s_latlong):
    '''
    The function takes a dataframe returned by find_nearby_places and outputs
    a list of
    CarouselColumns
    it uses linebot sdk module, for more details, see
    https://developers.line.biz/en/docs/messaging-api
    parameters:
    1. nearby_place_df : a pandas dataframe returned by the find_nearby_places
    function

    return values:
    1. normal : returns a list that contains CarouselColumns that can be used
    as a input in the
    make_nearby_carousel_template_column
    2. error : returns 'ERROR_OCCURED'
    '''
    try:
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
            distance = calculate_distance(s_latlong, nearby_place_df[i][4])
            column.append(CarouselColumn(
                title=title,
                text=text+f'\n{distance}公里(直線距離)',
                actions=[
                    PostbackTemplateAction(label='查看詳細資料', data=f'/detail/{nearby_place_df[i][2]}({nearby_place_df[i][0]})')    # noqa: E501
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
                quick_reply_lst.append(QuickReplyButton(action=PostbackAction(label=label_lst[i], data=text_lst[i])))    # noqa: E501
            return quick_reply_lst
        except Exception:
            return 'ERROR_OCCURED'
    else:
        return 'ERROR_OCCURED'


def make_bubble_component(place_name, detail_lst, now_latlong):
    openhr, address, phone, rate, price, latlong, photo = detail_lst[0], detail_lst[1], detail_lst[2], detail_lst[3], detail_lst[4], detail_lst[5], detail_lst[6]  # noqa: E501
    link = generate_guild_link(now_latlong, latlong)
    address_content = []
    address_content.append(IconComponent(url='https://cdn-icons-png.flaticon.com/512/235/235861.png',size='lg'))
    times = len(address) // 15 + 1
    for i in range(1, times+1):
        if i != times:
            address_content.append(TextComponent(text=f' {address[15*(i-1):15*i]}', size='md'))
        else:
            address_content.append(TextComponent(text=f' {address[15*(i-1):]}', size='md'))
    bubble = BubbleContainer(
        direction='ltr',
        header=BoxComponent(
            layout='vertical',
            contents=[
                TextComponent(
                    text=place_name,
                    weight='bold',
                    size='28px',
                ),
            ]
        ),
        hero=ImageComponent(
            url=f'https://maps.googleapis.com/maps/api/place/photo?maxwidth=800&photo_reference={photo}&key=AIzaSyDIX1tgCL2g8bS9o9rT50G8GyPvY1cBNFE',  # noqa: E501
            size='full'
        ),
        body=BoxComponent(
            layout='vertical',
            contents=[
                BoxComponent(
                    layout='baseline',
                    contents=[
                        IconComponent(
                            url='https://cdn-icons-png.flaticon.com/512/217/217887.png',  # noqa: E501
                            size='lg'
                        ),
                        TextComponent(
                            text=f'  {phone}',
                            size='lg'
                        )
                    ]
                ),
                BoxComponent(
                    layout='baseline',
                    contents=address_content
                ),
                BoxComponent(
                    layout='baseline',
                    contents=[
                        IconComponent(
                            url='https://img.tukuppt.com/ad_preview/00/31/67/ObvzW3N3kV.jpg!/both/260x260',    # noqa: E501
                            size='lg'
                        ),
                        TextComponent(
                            text=f'  {openhr}',
                            size='md'
                        )
                    ]
                ),
                BoxComponent(
                    layout='baseline',
                    contents=[
                        IconComponent(
                            url='https://cdn-icons-png.flaticon.com/512/3629/3629625.png',    # noqa: E501
                            size='lg'
                        ),
                        TextComponent(
                            text=f'  {rate}',
                            size='md'
                        ),
                        IconComponent(
                            url='https://cdn-icons-png.flaticon.com/512/189/189715.png',    # noqa: E501
                            size='lg'
                        ),
                        TextComponent(
                            text=f'  {price}',
                            size='md'
                        ),
                    ]
                ),
                BoxComponent(
                    layout='horizontal',
                    margin='xxl',
                    contents=[
                        ButtonComponent(
                            style='primary',
                            color='#FFC849',
                            height='sm',
                            action=URIAction(label='電話聯絡', uri=f'tel:{phone}'),
                        ),
                        ButtonComponent(
                            style='primary',
                            color='#748FFF',
                            height='sm',
                            action=URIAction(label='路線', uri=link),
                        )
                    ]
                )
            ]
        ),
    )
    return bubble
