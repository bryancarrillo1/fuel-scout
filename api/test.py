import geoapify as geo
import tollguru as tg

data = geo.get_route(27.9806068, -82.5151287, 29.6502046, -82.3416096)
coords = geo.get_coordinates(data)
props = geo.get_properties(data)

cost = tg.get_trip_cost(coords,props)

print(cost)