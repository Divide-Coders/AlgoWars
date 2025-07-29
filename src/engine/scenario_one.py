#Nima
#from asyncio import graph
from map.baseCity import BaseCity
from algorithms.pathfinding import shortest_path
#from visualizer.plot_attack_paths import plot_attack_paths
import json
import os

def save_attack_log(attack_log, scenario_name="scenario_1"):
    os.makedirs("results", exist_ok=True)
    with open(f"results/{scenario_name}.json", "w") as f:
        json.dump(attack_log, f, indent=4)
   # plot_attack_paths(graph, cities, attack_log)

def run_scenario(cities, 
                 missiles, 
                 graph):
    base_cities = []
    for c in cities:
        if c.city_type == "base":
            b = BaseCity(c.name, c.country, c.x, c.y, c.defense_level)
            base_cities.append(b)

    # sangar shekan  yeahhh buddy
    d_missiles = [m for m in missiles if m.category == "D1"]
    if not d_missiles:
        print("D1 Missile Not Found")
        return []  # Correct: return empty list

    # charge- Each base receives exactly two D1 missiles
    for base in base_cities:
        # For each base, we create two copies of the D1 missile.    
        base_missiles = []
        for _ in range(2):  # Exactly two missiles
            base_missiles.append(d_missiles[0])  # Add the same D1 missile twice
        
        base.load_missiles(base_missiles)
        print(f"   {base.name}: {len(base_missiles)} D1 missiles loaded")

    total_damage = 0
    attack_log = []

    for base in base_cities:
        for target in cities:
            if target.city_type != "enemy":
                continue

            missile = base.fire_missile()
            if missile is None:
                break
            path, dist = shortest_path(graph, 
                                       base.name, 
                                       target.name,
                                       missile.max_range)  
            if path is None:
                continue

            if missile.stealth > target.defense_level:
                damage = missile.damage
                total_damage += damage
                attack_log.append({
                    "from":   base.name,
                    "to":     target.name,
                    "path":   path,
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
        print("Attack Summary:")
        for log in attack_log:
            d = log.get("damage", 0)
            status = "Hit" if d > 0 else "Blocked"
            print(f"{log['from']} ->  {log['to']} | Path: {' -> '.join(log['path'])} | {status} | Damage: {d}")
    
    save_attack_log(attack_log)
    print(" Results saved to results/scenario_1.json")

    print(f"\n Total Damage: {total_damage}")                       
    
    return attack_log                       