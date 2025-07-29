import math

class Spy:
    def __init__(self, name, detection_range=100):
        self.name = name
        self.detection_range = detection_range  # Detection range in km
    
    def can_detect(self, missile_position):
        """Check if spy can detect missile at given position"""
        # Calculate distance between spy and missile
        # For simplicity, we'll use a basic distance calculation
        # In a real implementation, this would be more complex
        return True  # Placeholder - will be implemented based on actual missile tracking
    
    def get_detection_range(self):
        """Get spy's detection range"""
        return self.detection_range
    
    def __str__(self):
        return f"Spy {self.name} (Range: {self.detection_range}km)" 