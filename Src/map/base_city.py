from map.city import City

#Nima
class BaseCity(City) :
    def __init__(self, name, country, x, y, defense_level=0):
        super().__init__(name, country, x, y, city_type="base", defense_level=defense_level)
        self.missiles = []

    def load_missiles(self, missile_list):
        self.missiles = missile_list.copy()


    def fire_missile(self):
        if self.missiles:
            return self.missiles.pop(0)
        else:
            return None 