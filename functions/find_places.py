# 3rd party module
import requests
import pandas as pd
import time
from math import radians, cos, sin, asin, sqrt

# my module
from config import GOOGLE_MAPS_API_KEY


def find_nearby_places(catagory, latlong, rankby='distance', api_key=GOOGLE_MAPS_API_KEY):  # noqa: E501
    '''
    The function takes a set of latitude and longitude as a input and outputs
    the places nearby
    it uses google maps api nearby search, for more details, see
    https://developers.google.com/maps/documentation/places/web-service/search-nearby

    parameters:
    1.catagory : the catagory of places you want to find nearby,
    valid catagories see
    https://developers.google.com/maps/documentation/places/web-service/supported_types
    2.rankby : Specifies the order in which results are listed.
    (default : distance)
    Possible values : 'prominence', 'distance'
    3.api_key : the google map api key that is used to find places nearby
    4. latlong : the set of latitude and longitude used to find places
    nearby it
    the format should be 'latitude,longitude'

    return values :
    1. noraml : the function returns a dataframe that contains
    the 'name', 'vincinity', 'place_id'
    and 'photo_reference' of the places nearby
    2. exception :
    ZERO_RESULTS : no results found nearby
    INVALID_REQUEST : an error occured when finding
    '''
    if catagory == 'all':
        catagory = ''
    if rankby == 'distance':
        url = f'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={latlong}&key={api_key}&opennow&language=zh-TW&type={catagory}&rankby=distance'  # noqa: E501
    else:
        url = f'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={latlong}&key={api_key}&opennow&language=zh-TW&type={catagory}&radius=15000'  # noqa: E501
    response = requests.request("GET", url).json()
    if response['status'] == 'OK':
        names = []
        vicinities = []
        placeIDs = []
        photoIDs = []
        latlongs = []
        for i in range(len(response['results'])):
            name = response['results'][i]['name']
            vicinity = response['results'][i]['vicinity']
            placeID = response['results'][i]['place_id']
            lat = response['result']['geometry']['location']['lat']
            long = response['result']['geometry']['location']['lng']
            latlong = f'{lat},{long}'
            try:
                photoID = response['results'][i]['photos'][0]['photo_reference']  # noqa: E501
            except Exception:
                photoID = 'none'
            names.append(name)
            vicinities.append(vicinity)
            placeIDs.append(placeID)
            photoIDs.append(photoID)
            latlongs.append(latlong)
            df = pd.DataFrame(
                [names, vicinities, placeIDs, photoIDs, latlongs],
                index=['name', 'vincinity', 'place_id', 'photo_reference', 'latlong']
            )
        return df
    else:
        return response['status']


def find_place_details(placeId, api_key=GOOGLE_MAPS_API_KEY):
    url = f'https://maps.googleapis.com/maps/api/place/details/json?place_id={placeId}&key={api_key}&language=zH-TW'  # noqa: E501
    response = requests.request("GET", url).json()
    loc_time = time.localtime()
    openhr = response['result'].get('opening_hours', '無法取得營業時間')['weekday_text'][loc_time.tm_wday]  # noqa: E501
    address = response['result'].get('formatted_address', '無法取得地址')
    phone = response['result'].get('formatted_phone_number', '無法取得電話')
    lat = response['result']['geometry']['location']['lat']
    long = response['result']['geometry']['location']['lng']
    if phone != '無法取得電話':
        phone = phone.replace(' ', '')
    rate = response['result'].get('rating', '無法取得評分')
    price = response['result'].get('price_level', '無法取得價錢')
    latlong = f'{lat},{long}'
    result = [openhr, address, phone, rate, price, latlong]
    return result


def generate_guild_link(start_latlong, dest_latlong):
    link = f'https://www.google.com/maps/dir/{start_latlong}/{dest_latlong}'
    return link


def calculate_distance(s_latlong, d_latlong):
    start_lat = float(s_latlong.split(',')[0])
    start_long = float(s_latlong.split(',')[1])
    dest_lat = float(d_latlong.split(',')[0])
    dest_long = float(d_latlong.split(',')[1])
    start_lat, start_long, dest_lat, dest_long = map(radians, [start_lat, start_long, dest_lat, dest_long])  # noqa: E501
    # 半正矢公式
    dlon = start_long - dest_long
    dlat = start_lat - dest_lat
    a = sin(dlat/2)**2 + cos(start_lat) * cos(dest_lat) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371
    dis = round((c * r * 1000)/1000, 2)
    return dis
