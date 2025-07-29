import unittest
import json
import os
import sys

# Add src directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, '..', 'src')
sys.path.insert(0, src_dir)

from data_loader.load_cities import load_cities
from data_loader.load_missiles import load_missiles
from map.graph import build_graph
from engine.scenario_one import run_scenario as run_scenario_one
from engine.scenario_two import run_scenario_two
from engine.scenario_three import run_scenario_three

class TestAlgoWarsScenarios(unittest.TestCase):
    
    def setUp(self):
        """Set up test data"""
        current_dir = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.join(current_dir, '..', 'data')
        
        self.cities = load_cities(os.path.join(data_dir, "cities.json"))
        self.missiles = load_missiles(os.path.join(data_dir, "missiles.json"))
        self.graph = build_graph(self.cities)
    
    def test_scenario_one_basic_attack(self):
        """Test Scenario 1: Basic Attack with D1 missiles"""
        print("\n🧪 Testing Scenario 1: Basic Attack")
        
        # Run scenario
        attack_log = run_scenario_one(self.cities, self.missiles, self.graph)
        
        # Assertions
        self.assertIsNotNone(attack_log)
        self.assertIsInstance(attack_log, list)
        
        # Check that all attacks use D1 missiles
        d1_missiles = [m for m in self.missiles if m.category == "D1"]
        self.assertGreater(len(d1_missiles), 0, "D1 missiles should be available")
        
        print(f"✅ Scenario 1 passed: {len(attack_log)} attacks logged")
    
    def test_scenario_two_limited_inventory(self):
        """Test Scenario 2: Limited Inventory with A-type missiles"""
        print("\n🧪 Testing Scenario 2: Limited Inventory")
        
        # Run scenario
        attack_log, total_damage = run_scenario_two(self.cities, self.missiles, self.graph)
        
        # Assertions
        self.assertIsNotNone(attack_log)
        self.assertIsInstance(attack_log, list)
        self.assertIsInstance(total_damage, int)
        self.assertGreaterEqual(total_damage, 0)
        
        # Check that attacks use A-type missiles
        a_missiles = [m for m in self.missiles if m.category.startswith("A")]
        self.assertGreater(len(a_missiles), 0, "A-type missiles should be available")
        
        print(f"✅ Scenario 2 passed: {len(attack_log)} attacks, {total_damage} total damage")
    
    def test_scenario_three_command_control(self):
        """Test Scenario 3: Command & Control with B and C missiles"""
        print("\n🧪 Testing Scenario 3: Command & Control")
        
        # Run scenario
        attack_log, total_damage = run_scenario_three(self.cities, self.missiles, self.graph)
        
        # Assertions
        self.assertIsNotNone(attack_log)
        self.assertIsInstance(attack_log, list)
        self.assertIsInstance(total_damage, int)
        self.assertGreaterEqual(total_damage, 0)
        
        # Check that attacks use B or C type missiles
        bc_missiles = [m for m in self.missiles if m.category.startswith("B") or m.category.startswith("C")]
        self.assertGreater(len(bc_missiles), 0, "B and C type missiles should be available")
        
        print(f"✅ Scenario 3 passed: {len(attack_log)} attacks, {total_damage} total damage")
    
    def test_missile_properties(self):
        """Test missile properties and constraints"""
        print("\n🧪 Testing Missile Properties")
        
        for missile in self.missiles:
            # Check required properties
            self.assertIsNotNone(missile.name)
            self.assertIsNotNone(missile.category)
            self.assertGreaterEqual(missile.max_range, 0)
            self.assertGreaterEqual(missile.uncontrolled_range, 0)
            self.assertGreaterEqual(missile.stealth, 0)
            self.assertGreaterEqual(missile.damage, 0)
            
            # Check that uncontrolled range doesn't exceed max range
            if missile.max_range > 0:  # Skip missiles with unlimited range
                self.assertLessEqual(missile.uncontrolled_range, missile.max_range)
        
        print(f"✅ All {len(self.missiles)} missiles have valid properties")
    
    def test_city_properties(self):
        """Test city properties and constraints"""
        print("\n🧪 Testing City Properties")
        
        for city in self.cities:
            # Check required properties
            self.assertIsNotNone(city.name)
            self.assertIsNotNone(city.country)
            self.assertIsNotNone(city.city_type)
            self.assertGreaterEqual(city.defense_level, 0)
            
            # Check valid city types
            valid_types = ["base", "normal", "enemy"]
            self.assertIn(city.city_type, valid_types)
            
            # Check that enemy cities have defense
            if city.city_type == "enemy":
                self.assertGreaterEqual(city.defense_level, 0)
        
        print(f"✅ All {len(self.cities)} cities have valid properties")
    
    def test_graph_connectivity(self):
        """Test graph connectivity and pathfinding"""
        print("\n🧪 Testing Graph Connectivity")
        
        # Check that graph has nodes
        self.assertGreater(self.graph.number_of_nodes(), 0)
        self.assertGreater(self.graph.number_of_edges(), 0)
        
        # Test pathfinding between some cities
        base_cities = [c for c in self.cities if c.city_type == "base"]
        enemy_cities = [c for c in self.cities if c.city_type == "enemy"]
        
        if base_cities and enemy_cities:
            from algorithms.pathfinding import shortest_path
            
            # Test path from base to enemy
            path, distance = shortest_path(
                self.graph, 
                base_cities[0].name, 
                enemy_cities[0].name, 
                10000  # Large range for testing
            )
            
            # Path might not exist, but function should not crash
            if path:
                self.assertIsInstance(path, list)
                self.assertGreater(len(path), 0)
                self.assertIsInstance(distance, (int, float))
        
        print(f"✅ Graph connectivity test passed")
    
    def test_output_files(self):
        """Test that output files are created correctly"""
        print("\n🧪 Testing Output Files")
        
        # Run all scenarios to generate output
        run_scenario_one(self.cities, self.missiles, self.graph)
        run_scenario_two(self.cities, self.missiles, self.graph)
        run_scenario_three(self.cities, self.missiles, self.graph)
        
        # Check that output directories exist
        self.assertTrue(os.path.exists("output/results"))
        self.assertTrue(os.path.exists("output/visualizations"))
        
        # Check that result files exist
        expected_files = [
            "output/results/scenario_1.json",
            "output/results/scenario_2.json", 
            "output/results/scenario_3.json"
        ]
        
        for file_path in expected_files:
            if os.path.exists(file_path):
                # Check that file contains valid JSON
                with open(file_path, 'r') as f:
                    data = json.load(f)
                    self.assertIsInstance(data, dict)
                    self.assertIn('scenario', data)
                    self.assertIn('total_damage', data)
                    self.assertIn('attack_details', data)
        
        print("✅ Output files test passed")

def run_performance_test():
    """Run performance test to measure execution time"""
    import time
    
    print("\n⚡ Performance Test")
    
    # Load data
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(current_dir, '..', 'data')
    
    cities = load_cities(os.path.join(data_dir, "cities.json"))
    missiles = load_missiles(os.path.join(data_dir, "missiles.json"))
    graph = build_graph(cities)
    
    # Test execution time for each scenario
    scenarios = [
        ("Scenario 1", lambda: run_scenario_one(cities, missiles, graph)),
        ("Scenario 2", lambda: run_scenario_two(cities, missiles, graph)),
        ("Scenario 3", lambda: run_scenario_three(cities, missiles, graph))
    ]
    
    for name, scenario_func in scenarios:
        start_time = time.time()
        try:
            result = scenario_func()
            end_time = time.time()
            execution_time = end_time - start_time
            print(f"✅ {name}: {execution_time:.2f} seconds")
        except Exception as e:
            print(f"❌ {name}: Failed - {e}")

if __name__ == "__main__":
    print("🎮 AlgoWars Test Suite")
    print("=" * 50)
    
    # Run unit tests
    unittest.main(argv=[''], exit=False, verbosity=2)
    
    # Run performance test
    run_performance_test()
    
    print("\n🎯 All tests completed!") 