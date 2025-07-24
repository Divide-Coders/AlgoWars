from .city import City
class EnemyCity(City):
    def __init__(self, name, country, x, y, defense):
        super().__init__(name, country, x, y, city_type="enemy", defense_level=defense)