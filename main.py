#Nima
# lets go to first start this app

from map.city import City
from map.graph import build_graph

city1 = City("Tehran", "Iran", 0, 0, "base", 0)
city2 = City("TelAviv", "Israel", 3, 4, "enemy", 3)
city3 = City("Isfahan", "Iran", 2, 2, "base", 0)

cities = [city1, city2, city3]
G = build_graph(cities)

print("Nodes: ", G.nodes())
print("Edges: ")
for u, v, data in G.edges(data=True):
    print(f"{u} ↔ {v} = {data['weight']:.2f}")