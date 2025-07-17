#Nima
import networkx as nx 

def shortest_path(graph, start, end, max_range):
    try:
        path = nx.dijkstra_path(graph, start, end, max_range)
        distance = sum(graph[u][v]['weight'] for u, v in zip(path[:-1], path[1:]))
        if distance <= max_range:
            return path, distance
        else:
            return None,None
    except nx.NetworkXNoPath:
        return None, None