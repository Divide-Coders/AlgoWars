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

        #yeeeaaahhh Budddddyyy
    def distance(city1, city2):
        return sqrt((city1.x - city2.x) ** 2 + (city1.y - city2.y) ** 2)
    