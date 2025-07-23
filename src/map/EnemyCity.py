from city import City
class EnemyCity(City):
    def __init__(self,name, country, x, y, defense):
        super().__init__(name, country, x, y)
        self.defense = defense