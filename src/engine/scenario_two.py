from map.baseCity import BaseCity
from algorithms.pathfinding import shortest_path
from engine.missile_inventory import load_missile_inventory
import os
import json

def run_scenario_two(cities, missiles, graph):
    print(" Running Scenario 2...")

    inventory = load_missile_inventory("data/scenarios/scenario_2_missiles.json")

    base_cities = []
    for c in cities:
        if c.city_type == "base":
            base = BaseCity(c.name, c.country, c.x, c.y, c.defense_level)
            base_cities.append(base)

    a_missiles_all = [m for m in missiles if m.category.startswith("A")]


    missiles_to_use = []
    for m in a_missiles_all:
        count = inventory.get(m.category, 0)
        for _ in range(count):
            missiles_to_use.append(m)

    total_damage = 0
    attack_log = []
    used = 0

    for base in base_cities:
        for target in cities:
            if target.city_type != "enemy":
                continue
            if used >= len(missiles_to_use):
                break
            missile = missiles_to_use[used]
            used += 1

            path, dist = shortest_path(graph, base.name, target.name, missile.max_range)
            if not path:
                continue

            if missile.stealth > target.defense_level:
                damage = missile.damage
                total_damage += damage
                attack_log.append({
                    "from": base.name,
                    "to": target.name,
                    "path": path,
                    "damage": damage
                })
            else:
                attack_log.append({
                    "from": base.name,
                    "to": target.name,
                    "path": path,
                    "damage": 0,
                    "status": "intercepted"
                })

    print(" Scenario 2 Complete.")
    print(f" Total Damage: {total_damage}")
    return attack_log
