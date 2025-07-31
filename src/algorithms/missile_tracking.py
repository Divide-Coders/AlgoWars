"""
Missile tracking and spy detection simulation
"""

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

def find_safe_targets_with_spy_detection(graph, base, cities, missile):
    """
    Find safe targets considering both defense and spy detection
    """
    safe_targets = []
    cities_dict = {c.name: c for c in cities}
    
    for target in cities:
        if target.city_type != "enemy":
            continue
            
        # Find shortest path
        path, distance = graph.shortest_path(base.name, target.name, missile.max_range)
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

def reset_all_spies(cities):
    """
    Reset all spies in all cities (for new scenario)
    """
    for city in cities:
        city.reset_spies()

def print_spy_info(cities):
    """
    Print information about spies in all cities
    """
    print("\n=== SPY INFORMATION ===")
    for city in cities:
        if city.has_spy:
            print(f"{city.name}: {city.get_spy_info()}")
    print("=" * 30) 