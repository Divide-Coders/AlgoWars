#Nima
from abc import ABC

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

    def add_spy(self, spy):
        """Add a spy to this city"""
        self.spies.append(spy)

    def detect_missile(self, missile, missile_position):
        """Check if spies in this city can detect a missile"""
        detection_count = 0
        for spy in self.spies:
            if spy.can_detect(missile_position):
                detection_count += 1
        
        # If detection count reaches missile stealth level, missile is detected
        if detection_count >= missile.stealth:
            self.detected_missiles.append(missile)
            return True
        return False

    def can_reprogram_missile(self):
        """Check if this city can reprogram missiles (base or normal cities)"""
        return self.city_type in ["base", "normal"]

    def get_defense_capacity(self):
        """Get current defense capacity (how many missiles can be intercepted)"""
        return self.defense_level

    def intercept_missile(self, missile):
        """Try to intercept a missile. Returns True if successful."""
        if missile in self.detected_missiles and self.defense_level > 0:
            self.defense_level -= 1
            return True
        return False



              