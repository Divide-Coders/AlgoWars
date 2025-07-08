# ⚔️ AlgoWars
Graph-based strategy game driven by divide-and-conquer and smart pathfinding algorithms.


> A war strategy game powered by graph algorithms, AI techniques, and smart pathfinding — built with Python (or Go).

---

## 🎯 Concept

**Divide & Dominate** is a battle simulation game where countries are represented as nodes in a graph. Players must use algorithmic thinking to launch missile attacks, choose optimal paths, and manage limited resources. The gameplay is driven by classic and advanced algorithms including:

- 🔁 Divide and Conquer
- 📍 Dijkstra’s & A* Pathfinding
- 🧠 Basic AI decision-making
- 🗺️ Graph traversal and cost optimization

---

## 🛠️ Features

- 📌 **Graph-based world map**: each node is a country, each edge is a potential missile route.
- 🚀 **Multiple missile types**: each with different range, cost, and damage.
- 🧠 **Algorithmic strategy engine**: simulate and evaluate different attack plans.
- 🎮 **Turn-based gameplay** with dynamic threat assessment.
- 🎓 Designed as a course project for *Algorithm Design* class — but built with real-world logic.

---

## 📁 Project Structure

```bash
divide-and-dominate/
├── LICENSE
├── README.md
├── docs/
│   ├── design-doc.md
│   └── screenshots/
├── src/
│   ├── main.py / main.go
│   ├── game/
│   │   ├── map_loader.py
│   │   ├── missile.py
│   │   ├── country.py
│   │   └── engine.py
│   └── algorithms/
│       ├── dijkstra.py
│       ├── a_star.py
│       ├── divide_and_conquer.py
│       └── utils.py
├── assets/
│   ├── sounds/
│   └── images/
├── tests/
│   └── test_engine.py
└── requirements.txt / go.mod
