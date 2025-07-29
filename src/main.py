#Nima 
from data_loader.load_cities import load_cities
from data_loader.load_missiles import load_missiles
from map.graph import build_graph
from algorithms.pathfinding import shortest_path
from engine.scenario_one import run_scenario as run_scenario_one
from engine.scenario_two import run_scenario_two
from engine.scenario_three import run_scenario_three
from visualizer.plot_attack_paths import plot_attack_paths
import json
import os
import matplotlib.pyplot as plt
import networkx as nx

def create_output_directory():
    """Create output directory for results"""
    os.makedirs("output/results", exist_ok=True)
    os.makedirs("output/visualizations", exist_ok=True)

def save_scenario_results(scenario_name, attack_log, total_damage):
    """Save scenario results to output directory"""
    results = {
        "scenario": scenario_name,
        "total_damage": total_damage,
        "total_attacks": len(attack_log),
        "successful_attacks": len([log for log in attack_log if log.get("damage", 0) > 0]),
        "intercepted_attacks": len([log for log in attack_log if log.get("status") == "intercepted"]),
        "attack_details": attack_log
    }
    
    with open(f"output/results/{scenario_name}.json", "w") as f:
        json.dump(results, f, indent=4)
    
    print(f"Results saved to: output/results/{scenario_name}.json")

def visualize_graph_with_attacks(graph, cities, attack_logs, scenario_name):
    """Visualize graph with attack paths for a specific scenario"""
    try:
        # Create position dictionary only for nodes that exist in the graph
        pos = {}
        for city in cities:
            if city.name in graph.nodes():
                pos[city.name] = (city.x, city.y)

        # Create figure with better styling
        plt.figure(figsize=(16, 12))
        plt.style.use('default')
        
        # Create a subgraph with only nodes that have positions
        subgraph = graph.subgraph(pos.keys())
        
        # Draw the base graph with improved styling
        nx.draw_networkx_nodes(subgraph, pos, 
                              node_color='#E8F4FD', 
                              node_size=800,
                              alpha=0.8,
                              edgecolors='#B8D4E3',
                              linewidths=2)
        nx.draw_networkx_edges(subgraph, pos, 
                              edge_color='#D3D3D3', 
                              alpha=0.4,
                              width=1.5,
                              style='solid')
        nx.draw_networkx_labels(subgraph, pos, font_size=9, font_weight='bold')

        # Color nodes by type with better colors
        base_cities = [city for city in cities if city.city_type == "base" and city.name in pos]
        enemy_cities = [city for city in cities if city.city_type == "enemy" and city.name in pos]
        normal_cities = [city for city in cities if city.city_type == "normal" and city.name in pos]
        
        # Draw base cities in green with better styling
        base_pos = {city.name: pos[city.name] for city in base_cities}
        if base_pos:
            nx.draw_networkx_nodes(subgraph, base_pos, 
                                  node_color='#2E8B57', 
                                  node_size=1000,
                                  alpha=0.9,
                                  edgecolors='#1B4D3E',
                                  linewidths=3)
        
        # Draw enemy cities in red with better styling
        enemy_pos = {city.name: pos[city.name] for city in enemy_cities}
        if enemy_pos:
            nx.draw_networkx_nodes(subgraph, enemy_pos, 
                                  node_color='#DC143C', 
                                  node_size=900,
                                  alpha=0.9,
                                  edgecolors='#8B0000',
                                  linewidths=3)
        
        # Draw normal cities in blue with better styling
        normal_pos = {city.name: pos[city.name] for city in normal_cities}
        if normal_pos:
            nx.draw_networkx_nodes(subgraph, normal_pos, 
                                  node_color='#4682B4', 
                                  node_size=700,
                                  alpha=0.7,
                                  edgecolors='#2F4F4F',
                                  linewidths=2)

        # Draw attack paths with improved styling
        successful_attacks = 0
        intercepted_attacks = 0
        
        for log in attack_logs:
            path = log.get("path", [])
            if len(path) >= 2:
                damage = log.get("damage", 0)
                if damage > 0:
                    color = '#FF4500'  # Orange Red for successful attacks
                    width = 4
                    successful_attacks += 1
                else:
                    color = '#FFD700'  # Gold for intercepted attacks
                    width = 3
                    intercepted_attacks += 1
                
                # Draw path edges with curved lines
                for i in range(len(path) - 1):
                    u, v = path[i], path[i + 1]
                    if u in pos and v in pos:
                        nx.draw_networkx_edges(subgraph, pos, 
                                             edgelist=[(u, v)], 
                                             edge_color=color, 
                                             width=width,
                                             alpha=0.8,
                                             style='dashed',
                                             arrows=True,
                                             arrowstyle='->',
                                             arrowsize=15)

        # Add legend
        legend_elements = [
            plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='#2E8B57', 
                      markersize=15, label='Base Cities', markeredgecolor='#1B4D3E', markeredgewidth=2),
            plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='#DC143C', 
                      markersize=15, label='Enemy Cities', markeredgecolor='#8B0000', markeredgewidth=2),
            plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='#4682B4', 
                      markersize=12, label='Normal Cities', markeredgecolor='#2F4F4F', markeredgewidth=1),
            plt.Line2D([0], [0], color='#FF4500', linewidth=4, linestyle='--', 
                      label=f'Successful Attacks ({successful_attacks})'),
            plt.Line2D([0], [0], color='#FFD700', linewidth=3, linestyle='--', 
                      label=f'Intercepted Attacks ({intercepted_attacks})')
        ]
        
        plt.legend(handles=legend_elements, loc='upper left', bbox_to_anchor=(0, 1), 
                  fontsize=10, frameon=True, fancybox=True, shadow=True)

        # Add title with better styling
        plt.title(f"AlgoWars - {scenario_name}\nAttack Paths Visualization", 
                 fontsize=18, fontweight='bold', pad=20, color='#2F4F4F')
        
        # Add statistics text
        total_damage = sum(log.get("damage", 0) for log in attack_logs)
        stats_text = f"Total Damage: {total_damage:,}\nSuccessful Attacks: {successful_attacks}\nIntercepted Attacks: {intercepted_attacks}"
        plt.figtext(0.02, 0.02, stats_text, fontsize=12, bbox=dict(boxstyle="round,pad=0.3", 
                                                                     facecolor="white", alpha=0.8))
        
        plt.axis("off")
        plt.tight_layout()
        
        # Save visualization with better quality
        plt.savefig(f"output/visualizations/{scenario_name.lower().replace(' ', '_')}.png", 
                    dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
        print(f"🎨 Beautiful visualization saved to: output/visualizations/{scenario_name.lower().replace(' ', '_')}.png")
        
        plt.show()
        
    except Exception as e:
        print(f"⚠️  Visualization failed for {scenario_name}: {e}")
        print("Continuing without visualization...")

def print_game_summary(cities, missiles, graph):
    """Print a comprehensive game summary"""
    print("=" * 60)
    print("🎮 ALGOWARS - GAME SUMMARY")
    print("=" * 60)
    
    # Cities summary
    base_cities = [c for c in cities if c.city_type == "base"]
    enemy_cities = [c for c in cities if c.city_type == "enemy"]
    normal_cities = [c for c in cities if c.city_type == "normal"]
    
    print(f"\n🏙️  CITIES:")
    print(f"   Bases: {len(base_cities)} - {[c.name for c in base_cities]}")
    print(f"   Enemies: {len(enemy_cities)} - {[c.name for c in enemy_cities]}")
    print(f"   Normal: {len(normal_cities)} - {[c.name for c in normal_cities]}")
    
    # Missiles summary
    missile_types = {}
    for missile in missiles:
        category = missile.category
        if category not in missile_types:
            missile_types[category] = []
        missile_types[category].append(missile.name)
    
    print(f"\n🚀 MISSILES:")
    for category, names in missile_types.items():
        print(f"   {category}: {names}")
    
    # Graph summary
    print(f"\n🗺️  GRAPH:")
    print(f"   Nodes: {graph.number_of_nodes()}")
    print(f"   Edges: {graph.number_of_edges()}")
    
    print("=" * 60)

def main():
    """Main game execution"""
    print("🎮 Starting AlgoWars Simulation...")
    
    # Create output directories
    create_output_directory()
    
    # - Load Cities -
    cities = load_cities("data/cities.json")
    print("\n🏙️  Cities Loaded:")
    for city in cities:
        print(f"   {city.name} ({city.country}) - Type: {city.city_type} - Defense: {city.defense_level}")

    # - Load Missiles -
    missiles = load_missiles("data/missiles.json")
    print("\n🚀 Missiles Loaded:")
    for m in missiles:
        print(f"   {m.name} - Damage: {m.damage}, Stealth: {m.stealth}, Max Range: {m.max_range}")

    # - Build Graph -
    graph = build_graph(cities)
    print("\n🗺️  Graph Built:")
    print(f"   Nodes: {graph.number_of_nodes()}")
    print(f"   Edges: {graph.number_of_edges()}")

    # Print game summary
    print_game_summary(cities, missiles, graph)

    # - Sample Path Test -
    print("\n🧪 Sample Pathfinding Test:")
    start_city = "Hamedan"
    target_city = "TelAviv"
    sample_missile = missiles[0]  # First missile from list

    path, distance = shortest_path(graph, start_city, target_city, sample_missile.max_range)

    if path:
        print(f"   Path found from {start_city} to {target_city}: {' → '.join(path)}")
        print(f"   Total distance: {distance:.2f} km")
        if distance > sample_missile.uncontrolled_range:
            print(f"   Missile exceeds uncontrolled range ({sample_missile.uncontrolled_range} km) — needs reprogramming")
        else:
            print(f"   Within uncontrolled range — no reprogramming needed")

        # Check defense
        target_defense = next(c.defense_level for c in cities if c.name == target_city)
        if sample_missile.stealth > target_defense:
            print(f"   HIT SUCCESSFUL — Damage: {sample_missile.damage}")
        else:
            print(f"   Intercepted by enemy defense (defense level: {target_defense})")
    else:
        print(f"   No valid path found within range ({sample_missile.max_range} km)")

    # - Run All Scenarios -
    print("\n" + "=" * 60)
    print("🎯 RUNNING ALL SCENARIOS")
    print("=" * 60)
    
    # Scenario 1
    print("\n📋 SCENARIO 1: Basic Attack")
    print("-" * 40)
    attack_log_1 = run_scenario_one(cities, missiles, graph)
    if attack_log_1 is None:
        attack_log_1 = []
        print("⚠️  Scenario 1 returned no results")
    save_scenario_results("scenario_1", attack_log_1, sum(log.get("damage", 0) for log in attack_log_1))
    visualize_graph_with_attacks(graph, cities, attack_log_1, "Scenario 1")
    
    # Scenario 2
    print("\n📋 SCENARIO 2: Limited Inventory")
    print("-" * 40)
    attack_log_2, total_damage_2 = run_scenario_two(cities, missiles, graph)
    save_scenario_results("scenario_2", attack_log_2, total_damage_2)
    visualize_graph_with_attacks(graph, cities, attack_log_2, "Scenario 2")
    
    # Scenario 3
    print("\n📋 SCENARIO 3: Command & Control")
    print("-" * 40)
    attack_log_3, total_damage_3 = run_scenario_three(cities, missiles, graph)
    save_scenario_results("scenario_3", attack_log_3, total_damage_3)
    visualize_graph_with_attacks(graph, cities, attack_log_3, "Scenario 3")
    
    # Final Summary
    print("\n" + "=" * 60)
    print("🏆 FINAL RESULTS SUMMARY")
    print("=" * 60)
    
    total_damage_1 = sum(log.get("damage", 0) for log in attack_log_1)
    successful_1 = len([log for log in attack_log_1 if log.get("damage", 0) > 0])
    successful_2 = len([log for log in attack_log_2 if log.get("damage", 0) > 0])
    successful_3 = len([log for log in attack_log_3 if log.get("damage", 0) > 0])
    
    print(f"Scenario 1: {total_damage_1} damage | {successful_1} successful attacks")
    print(f"Scenario 2: {total_damage_2} damage | {successful_2} successful attacks")
    print(f"Scenario 3: {total_damage_3} damage | {successful_3} successful attacks")
    
    best_scenario = max([(total_damage_1, "Scenario 1"), 
                        (total_damage_2, "Scenario 2"), 
                        (total_damage_3, "Scenario 3")], 
                       key=lambda x: x[0])
    
    print(f"\n🏅 Best Performing Scenario: {best_scenario[1]} ({best_scenario[0]} damage)")
    print(f"📁 All results saved in: output/results/")
    print(f"🖼️  All visualizations saved in: output/visualizations/")
    
    print("\n🎮 AlgoWars Simulation Complete!")
    print("=" * 60)

if __name__ == "__main__":
    main()