#Nima

class City:
    def __init__(self, name, country, x, y):
        self.name = name      
        self.country = country
        self.x = x
        self.y = y
        self.has_py = False  # jassooss kasif

# ! I code it tomarrow please dont touch them
class EnemyCity(City):
    def __init__(self,defense):
        self.defense = defense

class OwnCity(City):
    def __init__(self,):
        pass

class BaseCity(OwnCity):
    def __init__(self,):
        pass

              