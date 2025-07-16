import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

def get_trip_cost(coords, props):
    """
    calculate trip cost including tolls and fuel using TollGuru API

    coords: list of coordinate tuples [(lon, lat), ...]
    props: dictionary with time (seconds) and distance
    
    returns dictionary with trip cost breakdown
    """
    tollguru_api_key = os.getenv('TOLLGURU_API_KEY')
    
    # convert coordinates to lat,lng path format for TollGuru
    path_coords = []
    for lon, lat in coords:
        path_coords.append(f"{lat},{lon}")
    
    path_string = "|".join(path_coords)

    url = "https://apis.tollguru.com/toll/v2/complete-polyline-from-mapping-service"
    
    payload = {
        "source": "here",
        "path": path_string,
        "vehicleType": "2AxlesAuto"
    }
    
    headers = {
        "x-api-key": tollguru_api_key,
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        
        if response.status_code != 200:
            print(f"TollGuru API error: {response.status_code}")
            print(f"Response: {response.text}")
            return None
            
        toll_data = response.json()
        
        route_data = toll_data.get("route", {})
        costs = route_data.get("costs", {})
        
        # get fuel cost from API 
        fuel_cost = costs.get("fuel", 0.0)
        
        toll_amount = 0.0
        has_tolls = route_data.get("hasTolls", False)
        
        if has_tolls:
            toll_amount = (costs.get("tag") or 
                          costs.get("cash") or 
                          costs.get("tagAndCash") or 
                          costs.get("minimumTollCost") or 
                          0.0)
        
        distance_data = route_data.get("distance", {})
        distance_meters = distance_data.get("value", 0)
        distance_miles = distance_meters / 1609.34  # meters to miles

        return {
            "distance_miles": round(distance_miles, 2),
            "duration_minutes": round(props["time"] / 60, 2),
            "fuel_cost_usd": round(fuel_cost, 2),
            "toll_cost_usd": round(toll_amount, 2),
            "total_cost_usd": round(fuel_cost + toll_amount, 2),
            "has_tolls": has_tolls,
            #"api_response": toll_data  # full response
        }
        
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None
