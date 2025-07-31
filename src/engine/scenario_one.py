#Nima
from map.baseCity import BaseCity
from algorithms.pathfinding import shortest_path
from algorithms.missile_tracking import (
    reset_all_spies,
    print_spy_info
)
import json
import os
import networkx as nx

def save_attack_log(attack_log, scenario_name="scenario_1"):
    os.makedirs("output/results", exist_ok=True)                     # Create output/results directory if it doesn't exist
    with open(f"output/results/{scenario_name}.json", "w") as f:    # Open the file for writing
        json.dump(attack_log, f, indent=4)

def is_safe_path(graph, path, cities_dict, missile_stealth):
    """
    Check if the path is safe for the missile (no cities with defense > missile stealth) # mohem
    """
    for city_name in path[1:-1]:  # Skip start and end cities  # :)
        city = cities_dict.get(city_name)
        if city and city.defense_level > missile_stealth:
            return False
    return True

def find_safe_targets_for_base(graph, base, cities, missile_stealth, missile_range):
    """
    Find all safe targets for a base with given missile specifications
    """
    safe_targets = []
    
    for target in cities:
        if target.city_type != "enemy":
            continue
            
        # Find shortest path
        path, distance = shortest_path(graph, base.name, target.name, missile_range)
        if path is None:
            continue
            
        # Check if path is safe (no cities with defense > missile stealth)
        if is_safe_path(graph, path, {c.name: c for c in cities}, missile_stealth):
            safe_targets.append({
                'target': target,
                'path': path,
                'distance': distance,
                'damage': missile_stealth > target.defense_level  # Will cause damage if stealth > defense
            })
    
    return safe_targets

def find_safe_targets_with_spies(graph, base, cities, missile):
    """
    Find safe targets considering both defense and spy detection
    """
    safe_targets = []
    cities_dict = {c.name: c for c in cities}
    
    for target in cities:
        if target.city_type != "enemy":
            continue
            
        # Find shortest path
        path, distance = shortest_path(graph, base.name, target.name, missile.max_range)
        if path is None:
            continue
            
        # Check if path is safe considering spies
        safe, reason = check_path_safety_with_spies(graph, path, cities_dict, missile)
        
        if safe:
            # Check if missile can hit target (stealth > defense)
            can_hit = missile.stealth > target.defense_level
            damage = missile.damage if can_hit else 0
            
            safe_targets.append({
                'target': target,
                'path': path,
                'distance': distance,
                'damage': damage,
                'can_hit': can_hit,
                'reason': reason
            })
        else:
            print(f"   Path to {target.name} not safe: {reason}")
    
    return safe_targets

def check_path_safety_with_spies(graph, path, cities_dict, missile):
    """
    Check if a path is safe considering both defense levels and spy detection
    Returns: (safe, reason)
    """
    # First check if path is safe from defense systems
    for city_name in path[1:-1]:  # Skip start and end cities
        city = cities_dict.get(city_name)
        if city and city.defense_level > missile.stealth:
            return False, f"City {city_name} has defense level {city.defense_level} > missile stealth {missile.stealth}"
    
    # Then simulate missile path to check for spy detection
    detected, detection_cities, detection_count = simulate_missile_path(graph, path, cities_dict, missile)
    
    if detected:
        return False, f"Missile detected by spies in cities: {detection_cities} (detection count: {detection_count} >= stealth: {missile.stealth})"
    
    return True, "Path is safe"

def simulate_missile_path(graph, path, cities_dict, missile):
    """
    Simulate missile traveling along a path and check for spy detection
    Returns: (detected, detection_cities, final_position)
    """
    detected = False
    detection_cities = []
    total_detection_count = 0
    
    # Track missile position along the path
    for i, city_name in enumerate(path):
        city = cities_dict.get(city_name)
        if not city:
            continue
            
        # Missile position at this city
        missile_position = (city.x, city.y)
        
        # Check if this city has spies that can detect the missile
        if city.has_spy:
            city.create_default_spy()  # Create default spy if needed
            detected_by_city, detection_count = city.detect_missile(missile, missile_position)
            
            if detected_by_city:
                detection_cities.append(city_name)
                total_detection_count += detection_count
                
                # If total detections reach missile stealth level, missile is detected
                if total_detection_count >= missile.stealth:
                    detected = True
                    break
    
    return detected, detection_cities, total_detection_count

def optimize_target_selection(safe_targets, max_missiles_per_base=2):
    """
    Optimize target selection to maximize total damage
    Prioritize targets that will cause damage (stealth > defense)
    """
    # Sort by potential damage (targets that will be hit first)
    damaging_targets = [t for t in safe_targets if t.get('can_hit', t.get('damage', False))]
    non_damaging_targets = [t for t in safe_targets if not t.get('can_hit', t.get('damage', False))]
    
    # Prioritize damaging targets
    selected_targets = damaging_targets[:max_missiles_per_base]
    
    # If we have slots left, add non-damaging targets
    remaining_slots = max_missiles_per_base - len(selected_targets)
    if remaining_slots > 0:
        selected_targets.extend(non_damaging_targets[:remaining_slots])
    
    return selected_targets

def run_scenario(cities, missiles, graph):
    """
    Run scenario 1: All bases have 2 D1 missiles, maximize damage
    """
    print("Running Scenario 1 with Spy Detection...")

    # Reset all spies for new scenario
    reset_all_spies(cities)
    
    # Print spy information
    print_spy_info(cities)

    # Find base cities
    base_cities = []
    for c in cities:
        if c.city_type == "base":
            b = BaseCity(c.name, c.country, c.x, c.y, c.defense_level)
            base_cities.append(b)

    # Find D1 missiles (SangarShekan)
    d_missiles = [m for m in missiles if m.category == "D1"]
    if not d_missiles:
        print("D1 Missile Not Found")
        return []

    d1_missile = d_missiles[0]
    print(f"Using missile: {d1_missile.name} (Damage: {d1_missile.damage}, Stealth: {d1_missile.stealth})")

    # Load exactly 2 D1 missiles for each base
    for base in base_cities:
        base_missiles = [d1_missile] * 2  # Exactly two missiles
        base.load_missiles(base_missiles)
        print(f"   {base.name}: {len(base_missiles)} D1 missiles loaded")

    total_damage = 0
    attack_log = []

    # Process each base
    for base in base_cities:
        print(f"\n--- Processing {base.name} ---")
        
        # Find all safe targets for this base (considering spies)
        safe_targets = find_safe_targets_with_spies(graph, base, cities, d1_missile)
        
        print(f"Found {len(safe_targets)} safe targets for {base.name}")
        
        # Optimize target selection (max 2 missiles per base)
        selected_targets = optimize_target_selection(safe_targets, max_missiles_per_base=2)
        
        print(f"Selected {len(selected_targets)} targets for {base.name}")
        
        # Execute attacks
        for target_info in selected_targets:
            missile = base.fire_missile()
            if missile is None:
                print(f"   No missiles left for {base.name}")
                break
                
            target = target_info['target']
            path = target_info['path']
            
            # Check if missile will hit (stealth > defense)
            if missile.stealth > target.defense_level:
                damage = missile.damage
                total_damage += damage
                status = "Hit"
                print(f"   {base.name} -> {target.name}: HIT! Damage: {damage}")
            else:
                damage = 0
                status = "Intercepted"
                print(f"   {base.name} -> {target.name}: INTERCEPTED! Defense: {target.defense_level}")
            
            attack_log.append({
                "from": base.name,
                "to": target.name,
                "path": path,
                "damage": damage,
                "status": status,
                "missile_stealth": missile.stealth,
                "target_defense": target.defense_level,
                "reason": target_info.get('reason', 'Safe path')
            })

    # Save results
    save_attack_log(attack_log)
    print(f"\nResults saved to output/results/scenario_1.json")
    print(f"Total Damage: {total_damage}")
    
    # Print summary
    print("\n=== ATTACK SUMMARY ===")
    for log in attack_log:
        print(f"{log['from']} -> {log['to']} | {log['status']} | Damage: {log['damage']}")
    
    return attack_log                       

