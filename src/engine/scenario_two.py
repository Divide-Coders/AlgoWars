from map.baseCity import BaseCity
from algorithms.pathfinding import shortest_path
from engine.missile_inventory import load_missile_inventory
import os
import json

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

    # توزیع موشک‌های A بین پایگاه‌ها
    a_missiles_all = [m for m in missiles if m.category.startswith("A")]
    
    # ایجاد لیست موشک‌ها بر اساس موجودی
    available_missiles = []
    for m in a_missiles_all:
        count = inventory.get(m.category, 0)
        for _ in range(count):
            available_missiles.append(m)
    
    # توزیع موشک‌ها بین پایگاه‌ها
    missiles_per_base = len(available_missiles) // len(base_cities)
    remainder = len(available_missiles) % len(base_cities)
    
    missile_index = 0
    for i, base in enumerate(base_cities):
        # تعداد موشک برای این پایگاه
        base_missile_count = missiles_per_base + (1 if i < remainder else 0)
        
        # تخصیص موشک‌ها به این پایگاه
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
        
        while base.missiles:
            missile = base.fire_missile()
            if missile is None:
                break
            
            # انتخاب بهترین هدف برای این موشک
            best_target = None
            best_path = None
            best_distance = float('inf')
            
            for target in cities:
                if target.city_type != "enemy":
                    continue
                    
                path, distance = shortest_path(graph, base.name, target.name, missile.max_range)
                if path and distance < best_distance:
                    best_target = target
                    best_path = path
                    best_distance = distance
            
            if best_target and best_path:
                # بررسی موفقیت حمله
                if missile.stealth > best_target.defense_level:
                    damage = missile.damage
                    total_damage += damage
                    successful_attacks += 1
                    
                    attack_log.append({
                        "from": base.name,
                        "to": best_target.name,
                        "missile": missile.name,
                        "path": best_path,
                        "damage": damage,
                        "status": "success"
                    })
                    
                    print(f"    {missile.name} → {best_target.name} | Damage: {damage}")
                else:
                    intercepted_attacks += 1
                    
                    attack_log.append({
                        "from": base.name,
                        "to": best_target.name,
                        "missile": missile.name,
                        "path": best_path,
                        "damage": 0,
                        "status": "intercepted"
                    })
                    
                    print(f"    {missile.name} → {best_target.name} | Intercepted (Defense: {best_target.defense_level})")
            else:
                print(f"    {missile.name} | Out of Range")
    
    print(f"\n=== Summary ===")
    print(f"Total Successful Attacks: {successful_attacks}")
    print(f"Total Intercepted Attacks: {intercepted_attacks}")

    print(" Scenario 2 Complete.")
    print(f" Total Damage: {total_damage}")
    return attack_log, total_damage
