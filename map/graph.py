#Nima
from map.city import City
from missiles.missile import Missile
import networkx as nx


def build_graph(cities):
    G = nx.Graph()
    for city in cities:
        G.add_node(city.name, pos=(city.x, city.y))
        for i in range(len(cities)):
            for j in range(i+1, len(cities)):
                c1, c2 = cities[i], cities[j]
                dist = Missile.distance(c1, c2)   #
                G.add_edge(c1.name, c2.name, weight= dist)
    return G