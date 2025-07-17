#Nima


class City:
    def __init__(self, name, country, x, y, city_type, defense=0):
        self.name = name      
        self.country = country
        self.x = x
        self.y = y
        self.city_type = city_type
        self.defense = defense
        self.has_py = False  #jassooss kasif

# ! I code it tomarrow please dont touch them
class EnemyCity(City):
    pass

class OwnCity(City):
    pass

class BaseCity(OwnCity):
    pass

              