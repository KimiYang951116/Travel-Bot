import requests
import pandas as pd
def  find_restaurant(api_key='AIzaSyDIX1tgCL2g8bS9o9rT50G8GyPvY1cBNFE', latlong = '24.985921220003803, 121.58641141745464', catagory='restaurant', radius=1500):
    url = f'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={latlong}&radius={radius}&key={api_key}&opennow&language=zh-TW&type={catagory}'
    response = requests.request("GET", url).json()
    if response['status'] == 'OK':
        rest_names = []
        rest_vicinities = []
        rest_placeIDs = []
        rest_photoIDs = []
        for i in range(len(response['results'])):
            rest_name = response['results'][i]['name']
            rest_vicinity = response['results'][i]['vicinity']
            rest_placeID = response['results'][i]['place_id']
            rest_photoID = response['results'][i]['photos'][0]['photo_reference']
            rest_names.append(rest_name)
            rest_vicinities.append(rest_vicinity)
            rest_placeIDs.append(rest_placeID)
            rest_photoIDs.append(rest_photoID)
            rest_df = pd.DataFrame([rest_names, rest_vicinities, rest_placeIDs, rest_photoIDs], index=['name', 'vincinity', 'place_id', 'photo_reference'])
        return rest_df
    elif response['status'] == 'ZERO_RESULTS':
        return '附近無餐廳'
    else:
        return '發生錯誤'