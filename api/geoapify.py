import requests
import os
from dotenv import load_dotenv

load_dotenv()

def get_route(start_lat, start_lon, end_lat, end_lon):
    ''' 
    returns response json containing data for trip 
    '''
    api_key = os.getenv('GEOAPIFY_API_KEY')

    url = "https://api.geoapify.com/v1/routing"
    
    params = {
        "waypoints": f"{start_lat},{start_lon}|{end_lat},{end_lon}",
        "mode": "drive",  
        "apiKey": api_key
    }

    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print("Error:", response.status_code, response.text)

def get_properties(data):
    ''' 
    takes in a json response and returns the properties (distance,time, etc.)
    '''

    feature = data["features"][0]
    props = feature["properties"]
    return props

def get_coordinates(data):
    ''' 
    takes in json response and returns list of coordinates to destination (geometry)
    '''

    feature = data["features"][0]
    coords = feature["geometry"]["coordinates"]

    if isinstance(coords[0][0], list):
        return [pt for line in coords for pt in line]
    else:
        return coords
 


