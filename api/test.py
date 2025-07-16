import geoapify as geo
import tollguru as tg

#get raw json response for route data
route_data = geo.get_route(27.9806068, -82.5151287, 28.428683, -81.306199)

#get coordinates and properties(distance/time)
coords = geo.get_coordinates(route_data)
props = geo.get_properties(route_data)

#get trip costs using tollguru
cost = tg.get_trip_cost(coords, props)

#find gas stations along route
fuel_stations = geo.get_fuel_stations_along_route(route_data)
fuel_coords = geo.get_fuel_coordinates(fuel_stations)
print(fuel_coords)

#print summary of gas stations found
geo.print_stations_summary(fuel_stations)