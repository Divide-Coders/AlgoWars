#Nima
import networkx as nx 

def shortest_path(graph, start, end, max_range):
    try:
        # ابتدا مسیر کوتاه‌ترین را پیدا می‌کنیم
        path = nx.dijkstra_path(graph, start, end, weight='weight')
        distance = sum(graph[u][v]['weight'] for u, v in zip(path[:-1], path[1:]))
        
        # بررسی محدودیت max_range (اگر max_range = -1 باشد، نامحدود است)
        if max_range == -1 or distance <= max_range:
            return path, distance
        else:
            return None, None
    except nx.NetworkXNoPath:
        return None, None