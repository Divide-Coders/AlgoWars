#Nima
from abc import ABC

class City(ABC):
    def __init__(self, name, country, x, y, city_type="normal", defense_level=0):
        self.name = name      
        self.country = country
        self.x = x
        self.y = y
        self.city_type = city_type
        self.defense_level = defense_level
        self.has_py = False  # jassooss kasif



              