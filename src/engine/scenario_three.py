from map.baseCity import BaseCity
from algorithms.pathfinding import shortest_path
from engine.missile_inventory import load_missile_inventory
import json
import os

def run_scenario_three(cities, missiles, graph):
    print("Running Scenario 3...")

    inventory = load_missile_inventory("data/scenarios/scenario_3_missiles.json")

    base_cities = []
    for c in cities:
        if c.city_type == "base":
            base = BaseCity(c.name, c.country, c.x, c.y, c.defense_level)