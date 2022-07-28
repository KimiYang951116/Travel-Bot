import requests
import json



LINE_API_KEY = '/NWkZeGHgzhXfj6UzLDYIf+xv5n3DHk4zB+YrNB2iIZafn55A44Eqfk3qOZClkK2webGFYYLpf5pQWGXzD0BKAJfJsJm8zDWyNSMnQ6pcgGwtF4j4hHelBnU5kgZUhP0TTiCXJ9fewaSpB+U4RIWawdB04t89/1O/w1cDnyilFU='  # noqa: E501
WEBHOOK_HANDLER = 'f28db6c57607c6e4a1b570b8294675cb'

headers = {"Authorization":f"Bearer {LINE_API_KEY}","Content-Type":"application/json"}

body = {
    "size": {"width": 2500, "height": 1686},
    "selected": "true",
    "name": "rich_menu_1",
    "chatBarText": "請分享你的位置",
    "areas":[
        {
          "bounds": {"x": 0, "y": 0, "width": 2500, "height": 1686},
          "action": {"type": "postback", "data": "如何分享位置"}
        }
    ]
  }

req = requests.request('POST', 'https://api.line.me/v2/bot/richmenu', 
                       headers=headers,data=json.dumps(body).encode('utf-8'))

print(req.text)
# richmenu-8fce423c47c1d11eed9a8074059b0780