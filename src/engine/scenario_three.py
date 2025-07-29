#Nima
from map.baseCity import BaseCity
from algorithms.pathfinding import shortest_path
from engine.missile_inventory import load_missile_inventory
import json
import os

def distribute_missiles_to_bases(bases, missile_inventory, missiles):
    """
    Distribution of missiles between bases based on divide and conquer algorithm
    """

    # Separation of B and C missiles
    b_missiles = [m for m in missiles if m.category.startswith("B")]
    c_missiles = [m for m in missiles if m.category.startswith("C")]
    
    # Creating a list of missiles based on inventory
    available_missiles = []
    
    # Adding B missiles
    for missile in b_missiles:
        count = missile_inventory.get(missile.category, 0)
        for _ in range(count):
            available_missiles.append(missile)
    
    # Adding C missiles
    for missile in c_missiles:
        count = missile_inventory.get(missile.category, 0)
        for _ in range(count):
            available_missiles.append(missile)
    
    # Distribution of missiles between bases equally
    missiles_per_base = len(available_missiles) // len(bases)
    remainder = len(available_missiles) % len(bases)
    
    missile_index = 0
    for i, base in enumerate(bases):
        # Number of missiles for this base
        base_missile_count = missiles_per_base + (1 if i < remainder else 0)
        
        # Assigning missiles to this base
        base_missiles = available_missiles[missile_index:missile_index + base_missile_count]
        base.load_missiles(base_missiles)
        missile_index += base_missile_count
        
        print(f"   {base.name}: {len(base_missiles)} missiles loaded")

def save_attack_log(attack_log, scenario_name="scenario_3"):
    """Save attack results to JSON file"""
    os.makedirs("results", exist_ok=True)
    with open(f"results/{scenario_name}.json", "w") as f:
        json.dump(attack_log, f, indent=4)

def run_scenario_three(cities, missiles, graph):
    """
    Scenario 3: Command
    - Distribution of B and C missiles between bases
    - Execution of simultaneous attacks from all bases
    """
    print("\n=== Scenario 3: Command ===")
    
    # Loading missile inventory
    missile_inventory = load_missile_inventory("src/engine/scenario_3_missiles.json")
    print(f"Missile Inventory: {missile_inventory}")
    
    # Identifying bases
    base_cities = []
    for city in cities:
        if city.city_type == "base":
            base = BaseCity(city.name, city.country, city.x, city.y, city.defense_level)
            base_cities.append(base)
    
    print(f"\nIdentified Bases: {len(base_cities)}")
    for base in base_cities:
        print(f"   {base.name}")
    
            # Distribution of missiles between bases
    print("\nDistribution of Missiles:")
    distribute_missiles_to_bases(base_cities, missile_inventory, missiles)
    
    # Identifying enemy targets
    enemy_cities = [city for city in cities if city.city_type == "enemy"]
    print(f"\nEnemy Targets: {len(enemy_cities)}")
    for enemy in enemy_cities:
        print(f"   {enemy.name} (Defense: {enemy.defense_level})")
    
    # Execution of attacks
    print("\n=== Starting Attacks ===")
    total_damage = 0
    attack_log = []
    successful_attacks = 0
    intercepted_attacks = 0
    
    for base in base_cities:
        print(f"\nAttack from {base.name}:")
        
        # لیست همه اهداف دشمن با اولویت‌بندی
        # اولویت‌بندی اهداف: اول اهداف با دفاع کم، سپس اهداف با آسیب بالا
        enemy_cities.sort(key=lambda x: (x.defense_level, -x.defense_level))  # اول کم‌ترین دفاع
        
        while base.missiles:
            missile = base.fire_missile()
            if missile is None:
                break
            
            # انتخاب بهترین هدف برای این موشک
            best_target = None
            best_path = None
            best_score = -1
            
            for target in enemy_cities:
                path, distance = shortest_path(graph, base.name, target.name, missile.max_range)
                if path:
                    # محاسبه امتیاز: آسیب احتمالی / (دفاع + 1)
                    potential_damage = missile.damage if missile.stealth > target.defense_level else 0
                    score = potential_damage / (target.defense_level + 1)
                    
                    if score > best_score:
                        best_score = score
                        best_target = target
                        best_path = path
            
            if best_target and best_path:
                # Checking the success of the attack
                if missile.stealth > best_target.defense_level:
                    damage = missile.damage
                    total_damage += damage
                    successful_attacks += 1
                    
                    attack_log.append({
                        "from": base.name,
                        "to": best_target.name,
                        "missile": missile.name,
                        "path": best_path,
                        "distance": distance,
                        "damage": damage,
                        "status": "success"
                    })
                    
                    print(f"    {missile.name} → {best_target.name} | Damage: {damage} (Score: {best_score:.1f})")
                else:
                    intercepted_attacks += 1
                    
                    attack_log.append({
                        "from": base.name,
                        "to": best_target.name,
                        "missile": missile.name,
                        "path": best_path,
                        "distance": distance,
                        "damage": 0,
                        "status": "intercepted"
                    })
                    
                    print(f"    {missile.name} → {best_target.name} | Intercepted (Defense: {best_target.defense_level})")
            else:
                print(f"    {missile.name} | No valid target found")
    
    # Summary of results
    print(f"\n=== Summary of Results ===")
    print(f"Total Successful Attacks: {successful_attacks}")
    print(f"Total Intercepted Attacks: {intercepted_attacks}")
    print(f"Total Damage: {total_damage}")
    
    # Saving results
    save_attack_log(attack_log)
    print(f"\nResults saved in results/scenario_3.json")
    
    return attack_log, total_damage
