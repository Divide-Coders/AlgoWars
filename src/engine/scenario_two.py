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
        
        # لیست همه اهداف دشمن با اولویت‌بندی
        enemy_targets = [city for city in cities if city.city_type == "enemy"]
        
        # اولویت‌بندی اهداف: اول اهداف با دفاع کم، سپس اهداف با آسیب بالا
        enemy_targets.sort(key=lambda x: (x.defense_level, -x.defense_level))  # اول کم‌ترین دفاع
        
        target_index = 0
        
        while base.missiles:
            missile = base.fire_missile()
            if missile is None:
                break
            
            # انتخاب بهترین هدف برای این موشک
            best_target = None
            best_path = None
            best_score = -1
            
            for target in enemy_targets:
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
                        
                    print(f"    {missile.name} → {best_target.name} | Damage: {damage} (Score: {best_score:.1f})")
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
                print(f"    {missile.name} | No valid target found")
    
    print(f"\n=== Summary ===")
    print(f"Total Successful Attacks: {successful_attacks}")
    print(f"Total Intercepted Attacks: {intercepted_attacks}")

    print(" Scenario 2 Complete.")
    print(f" Total Damage: {total_damage}")
    return attack_log, total_damage
