import sys
import os
sys.path.append('src')

from data_loader.load_cities import load_cities
from map.graph import build_graph
import networkx as nx
import matplotlib.pyplot as plt

# Load cities and build graph
cities = load_cities('data/cities.json')
graph = build_graph(cities)

print("Nodes in graph:", list(graph.nodes())[:10])
print("Shiraz in graph:", 'Shiraz' in graph.nodes())

# Check positions
for city in cities:
    if city.name == 'Shiraz':
        print(f"Shiraz position: ({city.x}, {city.y})")
        break

# Check which nodes have positions
pos = {}
for city in cities:
    if city.name in graph.nodes():
        pos[city.name] = (city.x, city.y)

print(f"Nodes with positions: {len(pos)}")
print(f"Nodes in graph: {len(graph.nodes())}")
print(f"Missing nodes: {set(graph.nodes()) - set(pos.keys())}")

# Test visualization
try:
    plt.figure(figsize=(12, 8))
    
    # Create a subgraph with only nodes that have positions
    subgraph = graph.subgraph(pos.keys())
    
    # Draw the base graph with only existing nodes
    nx.draw_networkx_nodes(subgraph, pos, 
                          node_color='lightblue', 
                          node_size=500,
                          alpha=0.7)
    nx.draw_networkx_edges(subgraph, pos, 
                          edge_color='gray', 
                          alpha=0.3,
                          width=1)
    nx.draw_networkx_labels(subgraph, pos, font_size=8)
    
    plt.title("Test Visualization")
    plt.axis("off")
    plt.tight_layout()
    
    print("✅ Visualization test successful!")
    plt.savefig("test_visualization.png", dpi=300, bbox_inches='tight')
    print("✅ Test visualization saved!")
    
except Exception as e:
    print(f"❌ Visualization test failed: {e}")
    import traceback
    traceback.print_exc() 