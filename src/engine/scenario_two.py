from map.baseCity import BaseCity
from algorithms.pathfinding import shortest_path
from engine.missile_inventory import load_missile_inventory
import os
import json
import random

def run_scenario_two(cities, missiles, graph):
    print(" Running Scenario 2...")

    inventory = load_missile_inventory("src/engine/scenario_2_missiles.json")
    print(f"Missile Inventory: {inventory}")

    base_cities = []
    for c in cities:
        if c.city_type == "base":
            base = BaseCity(c.name, c.country, c.x, c.y, c.defense_level)
            base_cities.append(base)

    print(f"Found {len(base_cities)} bases: {[b.name for b in base_cities]}")

    # Distribute A-type missiles between bases
    a_missiles_all = [m for m in missiles if m.category.startswith("A")]

    # Create a list of missiles based on inventory
    available_missiles = []
    for m in a_missiles_all:
        count = inventory.get(m.category, 0)
        for _ in range(count):
            available_missiles.append(m)
    
    # Distribute missiles between bases
    missiles_per_base = len(available_missiles) // len(base_cities)
    remainder = len(available_missiles) % len(base_cities)
    
    missile_index = 0
    for i, base in enumerate(base_cities):
        # Number of missiles for this base
        base_missile_count = missiles_per_base + (1 if i < remainder else 0)
        
        # Assign missiles to this base
        base_missiles = available_missiles[missile_index:missile_index + base_missile_count]
        base.load_missiles(base_missiles)
        missile_index += base_missile_count
        
        print(f"   {base.name}: {len(base_missiles)} A-type missiles loaded")

    total_damage = 0
    attack_log = []
    successful_attacks = 0
    intercepted_attacks = 0

    print(f"\n=== Starting Attacks ===")

    for base in base_cities:
        print(f"\nAttack from {base.name}:")
        
        # List of all enemy targets
        enemy_targets = [city for city in cities if city.city_type == "enemy"]
        
        # Priority of targets: first targets with low defense, then based on distance
        enemy_targets.sort(key=lambda x: (x.defense_level, 0))  # First lowest defense
        
        while base.missiles:
            missile = base.fire_missile()
            if missile is None:
                break
            
            # Select the best target for this missile
            best_target = None
            best_path = None
            best_score = -1
            
            # List of available targets
            available_targets = []
            for target in enemy_targets:
                path, distance = shortest_path(graph, base.name, target.name, missile.max_range)
                if path:
                    available_targets.append((target, path, distance))
            
            if available_targets:
                # Randomly select the top 3 targets
                available_targets.sort(key=lambda x: x[2])  # Based on distance
                top_targets = available_targets[:min(3, len(available_targets))]
                selected_target, selected_path, selected_distance = random.choice(top_targets)
                
                # Check the success of the attack
                if missile.stealth > selected_target.defense_level:
                    damage = missile.damage
                    total_damage += damage
                    successful_attacks += 1
                        
                    attack_log.append({
                        "from": base.name,
                            "to": selected_target.name,
                            "missile": missile.name,
                            "path": selected_path,
                            "damage": damage,
                            "status": "success"
                    })
                        
                    print(f"    {missile.name} -> {selected_target.name} | Damage: {damage}")
                else:
                    intercepted_attacks += 1
                    
                    attack_log.append({
                        "from": base.name,
                            "to": selected_target.name,
                            "missile": missile.name,
                            "path": selected_path,
                        "damage": 0,
                        "status": "intercepted"
                    })
                        
                    print(f"    {missile.name} -> {selected_target.name} | Intercepted (Defense: {selected_target.defense_level})")
            else:
                print(f"    {missile.name} | No valid target found")
    
    print(f"\n=== Summary ===")
    print(f"Total Successful Attacks: {successful_attacks}")
    print(f"Total Intercepted Attacks: {intercepted_attacks}")

    print(" Scenario 2 Complete.")
    print(f" Total Damage: {total_damage}")
    return attack_log, total_damage
