import matplotlib.pyplot as plt
import networkx as nx

def plot_attack_paths(graph, cities, attack_log):
    pos = {}
    for city in cities:
        pos[city.name] = (city.x, city.y)

    plt.figure(figsize=(10, 6))
    nx.draw_networkx(graph, pos, with_labels=True, node_color='lightblue', font_size=9)

    # Draw attack paths
    for log in attack_log:
        path = log["path"]
        color = 'red' if log.get("damage", 0) > 0 else 'gray'
        for u, v in zip(path[:-1], path[1:]):
            nx.draw_networkx_edges(graph, pos, edgelist=[(u, v)], edge_color=color, width=2)

    plt.title("Missile Attack Paths - Scenario 1")
    plt.axis("off")
    plt.tight_layout()
    plt.savefig("results/scenario_1.png")
    plt.show()
