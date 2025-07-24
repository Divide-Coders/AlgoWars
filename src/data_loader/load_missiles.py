from pathlib import Path
import json
from missiles.missile import Missile

def load_missiles(filepath):  
    filepath = Path(filepath)
    missiles = []  
    with open(filepath, 'r') as f:
        data = json.load(f)
        for item in data:
            m = Missile(
                name=item['name'],
                max_range=item['max_range'],
                uncontrolled_range=item['uncontrolled_range'],
                stealth=item['stealth'],
                damage=item['damage'],
                category=item['category']
            )
            missiles.append(m)
    return missiles
