#Nima
from math import sqrt
from map.city import City

class Missile:
    def __init__(self, name, max_range, uncontrolled_range, stealth, damage, category):
        self.name = name
        self.max_range = max_range
        self.uncontrolled_range = uncontrolled_range
        self.stealth = stealth
        self.damage = damage
        self.category = category
        self.current_position = None
        self.distance_traveled = 0
        self.is_detected = False
        self.needs_reprogramming = False

        #yeeeaaahhh Budddddyyy
    def distance(city1, city2):
        return sqrt((city1.x - city2.x) ** 2 + (city1.y - city2.y) ** 2)
    
    def launch(self, start_city):
        """Launch missile from a city"""
        self.current_position = (start_city.x, start_city.y)
        self.distance_traveled = 0
        self.is_detected = False
        self.needs_reprogramming = False
    
    def move_towards(self, target_city, distance):
        """Move missile towards target city"""
        if self.distance_traveled + distance > self.max_range:
            return False  # Missile would exceed max range
        
        self.distance_traveled += distance
        
        # Check if missile needs reprogramming
        if self.distance_traveled > self.uncontrolled_range:
            self.needs_reprogramming = True
        
        return True
    
    def can_reach_target(self, target_city):
        """Check if missile can reach target without exceeding max range"""
        distance_to_target = Missile.distance(
            City("temp", "temp", self.current_position[0], self.current_position[1]),
            target_city
        )
        return self.distance_traveled + distance_to_target <= self.max_range
    
    def reprogram(self):
        """Reprogram missile to reset uncontrolled range"""
        self.needs_reprogramming = False
        self.distance_traveled = 0  # Reset distance for new uncontrolled range
    
    def is_destroyed(self):
        """Check if missile is destroyed (exceeded max range)"""
        return self.distance_traveled > self.max_range
    
    def get_stealth_level(self):
        """Get missile's stealth level"""
        return self.stealth
    
    def get_damage(self):
        """Get missile's damage"""
        return self.damage
    