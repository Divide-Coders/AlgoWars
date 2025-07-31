import math

class Spy:
    def __init__(self, name, detection_range=100):
        self.name = name
        self.detection_range = detection_range  # Detection range in km
        self.detection_count = 0  # How many missiles this spy has detected
    
    def can_detect(self, missile_position, spy_position):
        """
        Check if spy can detect missile at given position
        missile_position: (x, y) coordinates of missile
        spy_position: (x, y) coordinates of spy
        """
        # Calculate distance between spy and missile
        dx = missile_position[0] - spy_position[0]
        dy = missile_position[1] - spy_position[1]
        distance = math.sqrt(dx*dx + dy*dy)
        
        return distance <= self.detection_range
    
    def detect_missile(self, missile, missile_position, spy_position):
        """
        Try to detect a missile. Returns True if detected.
        """
        if self.can_detect(missile_position, spy_position):
            self.detection_count += 1
            return True
        return False
    
    def get_detection_range(self):
        """Get spy's detection range"""
        return self.detection_range
    
    def get_detection_count(self):
        """Get number of missiles detected by this spy"""
        return self.detection_count
    
    def reset_detection_count(self):
        """Reset detection count (for new scenario)"""
        self.detection_count = 0
    
    def __str__(self):
        return f"Spy {self.name} (Range: {self.detection_range}km, Detected: {self.detection_count})" 