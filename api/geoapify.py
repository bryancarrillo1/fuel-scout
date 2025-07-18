import requests
import os
import math
import json
from dotenv import load_dotenv

load_dotenv()

def get_route(start_lat, start_lon, end_lat, end_lon):
    ''' 
    returns response json containing data for trip 
    '''
    api_key = os.getenv('GEOAPIFY_API_KEY')

    url = "https://api.geoapify.com/v1/routing"
    
    params = {
        "waypoints[0]": f"{start_lat},{start_lon}",
        "waypoints[1]": f"{end_lat},{end_lon}",
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
    takes in json response and returns list of coordinates to destination (geometry).
    Can be used to draw a polyline in leaflet.
    '''

    feature = data["features"][0]
    coords = feature["geometry"]["coordinates"]
    if isinstance(coords[0][0], list):
        flat_coords = [pt for line in coords for pt in line]
    else:
        flat_coords = coords
    return [coord[::-1] for coord in flat_coords]

def get_fuel_stations_along_route(route_data, search_radius=2000, point_interval=240):
    """
    find fuel stations along a route using circles with search radius (set to 2km by default) at specified interval
    """

    api_key = os.getenv('GEOAPIFY_API_KEY')
    
    coordinates = route_data
    print(f"Route has {len(coordinates)} coordinate points")
    
    sampled_coords = coordinates[::point_interval]
    print(f"Searching around {len(sampled_coords)} sampled points")
    
    all_stations = []
    
    for i, (lon, lat) in enumerate(sampled_coords):
        print(f"Searching point {i+1}/{len(sampled_coords)}: {lat}, {lon}")
        
        url = "https://api.geoapify.com/v2/places"
        
        params = {
            "categories": "service.vehicle.fuel",
            "filter": f"circle:{lon},{lat},{search_radius}",
            "bias": f"proximity:{lon},{lat}",
            "limit": 50,
            "apiKey": api_key
        }
        
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            data = response.json()
            features = data.get("features", [])
            print(f"  Found {len(features)} stations at this point")
            
            for feature in features:
                all_stations.append(feature)

        else:
            print(f"  Error at point {lat},{lon}:", response.status_code, response.text)
    
    print(f"Total stations found: {len(all_stations)}")
    return {"type": "FeatureCollection", "features": all_stations}

def get_fuel_coordinates(stations_data):
    """
    Extracts coordinates from the fuel stations data
    and returns a list [lon, lat]. Can be used to draw pins in leaflet
    """
    features = stations_data.get("features", [])
    coords = []
    
    for feature in features:
        coord = feature.get("geometry", {}).get("coordinates", [])
        coords.append([round(coord[1],6), round(coord[0],6)])  # [lat, lon] format for Leaflet   
    return coords

def print_stations_summary(stations_data):
    """
    helper function to print a summary of the fuel stations found (for debugging)
    """   
    features = stations_data.get("features", [])
    
    print(f"\n Fuel Stations Found: ({len(features)}) ")
    
    for i, station in enumerate(features, 1):
        props = station.get("properties", {})
        coords = station.get("geometry", {}).get("coordinates", [])
        
        print(f"\n{i}. {props.get('name', 'Unknown Station')}")
        print(f"   Brand: {props.get('brand', 'N/A')}")
        print(f"   Address: {props.get('formatted', 'N/A')}")
        print(f"   Coordinates: {coords[1]:.6f}, {coords[0]:.6f}")