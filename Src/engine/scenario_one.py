from map.base_city import BaseCity
from algorithms.pathfinding import shortest_path

def run_scenario(cities, missiles, graph) -> None:
    base_cities = []
    for c in cities:
        if c.city_type == "base":
            b = BaseCity(c.name, c.country, c.x, c.y, c.defense_level)
            base_cities.append(b)

    # sangar shekan  yeahhh buddy
    d = [m for m in missiles if m.category == "D1"]
    if not d:
        print("D1 Missile Not Found")
        return

    # charge
    for base in base_cities:
        base.load_missiles(d)

    total_damage = 0
    attack_log = []
               