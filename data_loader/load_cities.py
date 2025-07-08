#Nima
import json
from map.city import City

def load_cities(filepath):
    cities = []
    with open(filepath, 'r') as f:
        data = json.load(f)
        for item in data:
            city = City(
                name=item['name'],
                country=item['country'],
                x=item['x'],
                y=item['y'],
                city_type=item['type'],
                defense=item['defense']
            )
            cities.append(city)
    return cities
