#Nima
from abc import ABC
from map.spy import Spy

class City:
    def __init__(self, name, country, x, y, city_type="normal", defense_level=0):
        self.name = name
        self.country = country
        self.x = x
        self.y = y
        self.city_type = city_type
        self.defense_level = defense_level
        self.spies = []  # List of spies in this city
        self.detected_missiles = []  # Missiles detected by spies in this city
        self.has_spy = False  # Whether this city has spies

    def add_spy(self, spy):
        """Add a spy to this city"""
        self.spies.append(spy)
        self.has_spy = True

    def create_default_spy(self):
        """Create a default spy for this city if it has spies"""
        if self.has_spy and not self.spies:
            default_spy = Spy(f"Spy_{self.name}", detection_range=50)
            self.spies.append(default_spy)

    def detect_missile(self, missile, missile_position):
        """
        Check if spies in this city can detect a missile
        missile_position: (x, y) coordinates of missile
        Returns: (detected, detection_count)
        """
        if not self.has_spy or not self.spies:
            return False, 0
        
        detection_count = 0
        spy_position = (self.x, self.y)
        
        for spy in self.spies:
            if spy.detect_missile(missile, missile_position, spy_position):
                detection_count += 1
        
        # If detection count reaches missile stealth level, missile is detected
        detected = detection_count >= missile.stealth
        if detected:
            self.detected_missiles.append(missile)
        
        return detected, detection_count

    def can_reprogram_missile(self):
        """Check if this city can reprogram missiles (base or normal cities)"""
        return self.city_type in ["base", "normal"]

    def get_defense_capacity(self):
        """Get current defense capacity (how many missiles can be intercepted)"""
        return self.defense_level

    def intercept_missile(self, missile):
        """
        Try to intercept a detected missile. Returns True if successful.
        """
        if missile in self.detected_missiles and self.defense_level > 0:
            self.defense_level -= 1
            return True
        return False

    def reset_spies(self):
        """Reset all spies in this city (for new scenario)"""
        for spy in self.spies:
            spy.reset_detection_count()
        self.detected_missiles.clear()

    def get_spy_info(self):
        """Get information about spies in this city"""
        if not self.has_spy:
            return "No spies"
        
        spy_info = []
        for spy in self.spies:
            spy_info.append(str(spy))
        return ", ".join(spy_info)



              