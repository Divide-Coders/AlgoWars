from pathlib import Path
import json
from map.city import City
from map.baseCity import BaseCity
from map.EnemyCity import EnemyCity


def load_cities(filepath):
    filepath = Path(filepath)
    cities = []
    with open(filepath, 'r') as f:
        data = json.load(f)
        for item in data:
            city_type = item.get('type', 'normal')
            if city_type == 'base':
                city = BaseCity(
                    name=item['name'],
                    country=item['country'],
                    x=item['x'],
                    y=item['y'],
                    defense_level=item.get('defense', 0)
                )
            elif city_type == 'enemy':
                city = EnemyCity(
                    name=item['name'],
                    country=item['country'],
                    x=item['x'],
                    y=item['y'],
                    defense=item.get('defense', 0)
                )
            else:
                city = City(
                    name=item['name'],
                    country=item['country'],
                    x=item['x'],
                    y=item['y']
                )
            city.has_spy = item.get('has_spy', False)  # optional
            city.city_type = city_type
            city.defense_level = item.get('defense', 0)
            cities.append(city)
    return cities
