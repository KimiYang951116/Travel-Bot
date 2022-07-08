# from audioop import add
# from importlib.resources import contents
# from linecache import lazycache
# from find_places import find_restaurant
# from flask import Flask, request, abort
# app = Flask(__name__)
# import requests
# import time
# from linebot import LineBotApi, WebhookHandler
# from linebot.exceptions import InvalidSignatureError
# from linebot.models import URITemplateAction, URIAction, ButtonComponent, FlexSendMessage, IconComponent, ImageComponent, TextComponent, BoxComponent, BubbleContainer, MessageTemplateAction, CarouselTemplate, CarouselColumn, MessageEvent, TextMessage, LocationMessage, TextSendMessage, QuickReply, QuickReplyButton, MessageAction, ImageSendMessage, StickerSendMessage, LocationSendMessage, TemplateSendMessage
# line_bot_api = LineBotApi('/NWkZeGHgzhXfj6UzLDYIf+xv5n3DHk4zB+YrNB2iIZafn55A44Eqfk3qOZClkK2webGFYYLpf5pQWGXzD0BKAJfJsJm8zDWyNSMnQ6pcgGwtF4j4hHelBnU5kgZUhP0TTiCXJ9fewaSpB+U4RIWawdB04t89/1O/w1cDnyilFU=')
# handler = WebhookHandler('f28db6c57607c6e4a1b570b8294675cb')
# @app.route("/callback", methods=['POST'])
# def callback():
#     signature = request.headers['X-Line-Signature']
#     body = request.get_data(as_text=True)
#     try:
#         handler.handle(body, signature)
#     except InvalidSignatureError:
#         abort(400)
#     return 'ok'
# @handler.add(MessageEvent, message=TextMessage)
# def handle_message(event):
#     etext = event.message.text
#     if etext.startswith('/detail') == True:
#         proetext = etext.split('/')
#         place_id = etext.split('/')[2].split('(')[0]
#         etextname = etext.split('(')[1].split(')')[0]

#         url = f'https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&key=AIzaSyCeN9OYJVZI-OslW5DfxFoKN0ZOK5Dtyzo&language=zH-TW'
#         payload={}
#         headers = {}

#         response = requests.request("GET", url, headers=headers, data=payload).json()
#         lo = time.localtime()
#         try:
#             openhr = response['result']['opening_hours']['weekday_text'][lo.tm_wday]
#         except:
#             openhr = '無法取得營業時間'
#         try:
#             address = response['result']['formatted_address']
#         except:
#             address = '無法取得地址'
#         try:
#             phone = response['result']['formatted_phone_number']
#             phone = phone.replace(' ', '')
#         except:
#             phone = '無法取得電話'
#         try:
#             rate = response['result']['rating']
#         except:
#             rate = '無法取得評分'
#         try:
#             price = response['result']['price_level']
#         except:
#             price = '無法取得價錢'
#         if len(address) > 14:
#             address1 = address[:14]
#             address2 = address[14:]
#         else:
#             address1 = address
#             address2 = ''
#         bubble = BubbleContainer(
#             direction = 'ltr',
#             header = BoxComponent(
#                 layout = 'vertical',
#                 contents = [
#                     TextComponent(
#                         text = etextname,
#                         weight = 'bold',
#                         size = 'xxl'
#                     ),
#                 ]
#             ),
#             hero = ImageComponent(
#                 url = 'https://bouchonbendigo.com.au/wp-content/uploads/2022/03/istockphoto-1316145932-170667a.jpg',
#                 size = 'full',
#             ),
#             body = BoxComponent(
#                 layout = 'vertical',
#                 contents = [
#                     BoxComponent(
#                         layout = 'baseline',
#                         contents = [
#                             IconComponent(
#                                 url = 'https://cdn-icons-png.flaticon.com/512/217/217887.png',
#                                 size = 'lg'
#                             ),
#                             TextComponent(
#                                 text = f'  {phone}',
#                                 size = 'lg'
#                             )
#                         ]
#                     ),
#                     BoxComponent(
#                         layout = 'baseline',
#                         contents = [
#                             IconComponent(
#                                 url = 'https://cdn-icons-png.flaticon.com/512/235/235861.png',
#                                 size = 'lg'
#                             ),
#                             TextComponent(
#                                 text = f'  {address1}',
#                                 size = 'md'
#                             )
#                         ]
#                     ),
#                     BoxComponent(
#                         layout = 'baseline',
#                         contents = [
#                             TextComponent(
#                                 text = f'  {address2}',
#                                 size = 'md'
#                             )
#                         ]
#                     ),
#                     BoxComponent(
#                         layout = 'baseline',
#                         contents = [
#                             IconComponent(
#                                 url = 'https://img.tukuppt.com/ad_preview/00/31/67/ObvzW3N3kV.jpg!/both/260x260',
#                                 size = 'lg'
#                             ),
#                             TextComponent(
#                                 text = f'  {openhr}',
#                                 size = 'md'
#                             )
#                         ]
#                     ),
#                     BoxComponent(
#                         layout = 'baseline',
#                         contents = [
#                             IconComponent(
#                                 url = 'https://cdn-icons-png.flaticon.com/512/3629/3629625.png', 
#                                 size = 'lg'
#                             ),
#                             TextComponent(
#                                 text = f'  {rate}',
#                                 size = 'md'
#                             ),
#                             IconComponent(
#                                 url = 'https://cdn-icons-png.flaticon.com/512/189/189715.png', 
#                                 size = 'lg'
#                             ),
#                             TextComponent(
#                                 text = f'  {price}',
#                                 size = 'md'
#                             ),
#                         ]
#                     ),
#                     BoxComponent(
#                         layout = 'horizontal',
#                         margin = 'xxl',
#                         contents = [
#                             ButtonComponent(
#                                 style = 'primary',
#                                 height = 'sm',
#                                 action = URIAction(label = '電話聯絡', uri = f'tel:{phone}'),
#                             ),
#                             ButtonComponent(
#                                 style = 'secondary',
#                                 height = 'sm',
#                                 action = URIAction(label = '查看路線', uri = 'https://meet.google.com/csr-igzo-tjs')
#                             )
#                         ]
#                     )
                    
#                 ]
#             ),


#         )
#         message = FlexSendMessage(alt_text = '彈性配置', contents=bubble)
#         line_bot_api.reply_message(event.reply_token, message)

        
# @handler.add(MessageEvent, message=LocationMessage)
# def handle_message(event):
#     connection = pymysql.connect(
#         host="us-cdbr-east-05.cleardb.net",
#         user="b5f2e205874506",
#         password="3291697e",
#         db="heroku_b2cccf87a825db4",
#         charset='utf8mb4',
#         cursorclass=pymysql.cursors.DictCursor
#     )
#     user_id = event.source.user_id
#     is_agree = GetUserInfo(connection, user_id, 'service')
#     if is_agree == 0:
#         mutimessage = []
#         mutimessage.append(TextSendMessage(text='''你尚未同意我們的使用條款，請先同意我們的條款
#         條款網址如下'''))
#         mutimessage.append(TextSendMessage(text='shorturl.at/fotLM'))
    
















#     # longitude = event.message.longitude
#     # latitude = event.message.latitude
#     # latlong = f'{latitude},{longitude}'
#     # rest_result= find_restaurant()
#     # if rest_result == '附近無餐廳':
#     #     line_bot_api.reply_message(event.reply_token, TextSendMessage(text='附近無餐廳'))
#     # elif rest_result == '發生錯誤':
#     #     line_bot_api.reply_message(event.reply_token, TextSendMessage(text='發生錯誤'))
#     # else:
#     #     rest_lst =  rest_result.values.tolist()
#     #     if len(rest_lst[0]) > 10:
#     #         times = 10
#     #     else:
#     #         times = len(rest_lst[0])
        




#     #     if len(placelst) > 10:
#     #         times = 10
#     #     else:
#     #         times = len(placelst)
#     #     for i in range(times):
column.append(CarouselColumn(
    thumbnail_image_url = 'https://thumbs.dreamstime.com/z/under-development-concept-illustration-large-billboard-construction-cranes-isolated-white-d-render-graphic-36929326.jpg',
    title=placelst[i],
    text = response['results'][i]['vicinity'],
    actions = [
        MessageTemplateAction(
            label = '查看詳細資料',
            text = f'/detail/{placeIDlst[i]}({placelst[i]})'
        )
    ]
))
#     #     print(column)
message = TemplateSendMessage(
    alt_text = '轉盤樣板',
    template=CarouselTemplate(
        columns=column
    ))
#     #     line_bot_api.reply_message(event.reply_token, message)
#     # elif response['status'] == 'ZERO_RESULTS':
#     #     line_bot_api.reply_message(event.reply_token, TextSendMessage(text='附近無餐廳'))
#     # elif response['status'] == 'INVALID_REQUEST':
#     #     line_bot_api.reply_message(event.reply_token, TextSendMessage(text='發生錯誤'))
    

if __name__ == '__main__':
    app.run()