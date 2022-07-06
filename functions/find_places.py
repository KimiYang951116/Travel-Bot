# 3rd party module
import requests
import pandas as pd

# my module
from config import GOOGLE_MAPS_API_KEY


def  find_nearby_places(catagory, latlong, rankby = 'distance', api_key=GOOGLE_MAPS_API_KEY, ):
    '''
    The function takes a set of latitude and longitude as a input and outputs the places nearby
    it uses google maps api nearby search, for more details, see 
    https://developers.google.com/maps/documentation/places/web-service/search-nearby
    
    parameters:
    1.catagory : the catagory of places you want to find nearby, 
    valid catagories see https://developers.google.com/maps/documentation/places/web-service/supported_types
    2.rankby : Specifies the order in which results are listed. (default : distance)
    Possible values : 'prominence', 'distance'
    3.api_key : the google map api key that is used to find places nearby
    4. latlong : the set of latitude and longitude used to find places nearby it
    the format should be 'latitude,longitude'

    return values : 
    1. noraml : the function returns a dataframe that contains the 'name', 'vincinity', 'place_id'
    and 'photo_reference' of the places nearby
    2. exception : 
    ZERO_RESULTS : no results found nearby
    INVALID_REQUEST : an error occured when finding
    '''
    if rankby == 'distance':
        url = f'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={latlong}&key={api_key}&opennow&language=zh-TW&type={catagory}&rankby=distance'
    else:
        url = f'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={latlong}&key={api_key}&opennow&language=zh-TW&type={catagory}&radius=15000'
    response = requests.request("GET", url).json()
    if response['status'] == 'OK':
        names = []
        vicinities = []
        placeIDs = []
        photoIDs = []
        for i in range(len(response['results'])):
            name = response['results'][i]['name']
            vicinity = response['results'][i]['vicinity']
            placeID = response['results'][i]['place_id']
            try:
                photoID = response['results'][i]['photos'][0]['photo_reference']
            except:
                photoID = 'none'
            names.append(name)
            vicinities.append(vicinity)
            placeIDs.append(placeID)
            photoIDs.append(photoID)
            df = pd.DataFrame([names, vicinities, placeIDs, photoIDs], index=['name', 'vincinity', 'place_id', 'photo_reference'])
        return df
    else:
        return response['status']
  