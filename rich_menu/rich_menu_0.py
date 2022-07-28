import requests
import json
from config import LINE_API_KEY



headers = {"Authorization":f"Bearer {LINE_API_KEY}","Content-Type":"application/json"}

body = {
    "size": {"width": 2500, "height": 1686},
    "selected": "true",
    "name": "rich_menu_0",
    "chatBarText": "請完成基本設定",
    "areas":[
        {
          "bounds": {"x": 0, "y": 0, "width": 2500, "height": 1686},
          "action": {"type": "postback", "data": "開始使用TravelBot"}
        }
    ]
  }

req = requests.request('POST', 'https://api.line.me/v2/bot/richmenu', 
                       headers=headers,data=json.dumps(body).encode('utf-8'))

print(req.text)

# richmenu-8f3bec982eb2b920d60519b5cfbc22a3