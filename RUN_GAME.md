# 🎮 AlgoWars - Game Runner

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Game
```bash
python src/main.py
```

## 📋 What the Game Does

The updated `main.py` now provides a comprehensive simulation that:

### 🎯 **Runs All Three Scenarios:**
- **Scenario 1**: Basic attack with D1 missiles
- **Scenario 2**: Limited inventory with A-type missiles  
- **Scenario 3**: Command & Control with B and C missiles

### 📊 **Generates Comprehensive Output:**
- **Results**: All scenario results saved in `output/results/`
- **Visualizations**: Attack path graphs saved in `output/visualizations/`
- **Summary**: Final comparison of all scenarios

### 🗺️ **Visualizes the Game:**
- **Green nodes**: Base cities (attackers)
- **Red nodes**: Enemy cities (targets)
- **Blue nodes**: Normal cities
- **Red dashed lines**: Successful attacks
- **Orange dashed lines**: Intercepted attacks

## 📁 Output Structure

```
output/
├── results/
│   ├── scenario_1.json
│   ├── scenario_2.json
│   └── scenario_3.json
└── visualizations/
    ├── scenario_1.png
    ├── scenario_2.png
    └── scenario_3.png
```

## 🏆 Game Features

- **Divide & Conquer**: Missile distribution algorithm
- **Pathfinding**: Dijkstra's algorithm for optimal routes
- **Strategy**: Multiple attack scenarios
- **Visualization**: Interactive graph plots
- **Analysis**: Comprehensive damage and success statistics

## 🎮 Game Summary

The game will show:
- City and missile loading
- Graph construction
- Sample pathfinding test
- All three scenario executions
- Final results comparison
- Best performing scenario identification

Enjoy the war simulation! ⚔️ 