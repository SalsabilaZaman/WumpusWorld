# Wumpus World Logical Agent

## Overview

This project simulates the navigation of a logical agent in the Wumpus World environment using logical representation and inference techniques. It is developed as part of the **CSE 604: Artificial Intelligence** course to explore how intelligent agents can reason and make decisions in uncertain and dangerous environments.

The Wumpus World is a grid-based environment inspired by Section 7.2 of Russell and Norvig’s AI textbook, where an agent must locate gold while avoiding deadly pits and the Wumpus creature. Our implementation uses a **10x10 grid** instead of the original smaller layout to enhance complexity and depth.

---

## Features

- ✅ Logical reasoning using **Propositional Logic** or **First Order Logic (FOL)**
- ✅ Flexible loading of environments: both **randomly generated** and **pre-defined maps**
- ✅ Representation of the environment and agent's knowledge base
- ✅ Inference mechanisms: **resolution**, **forward chaining**, **backward chaining**
- ✅ Optional integration of **probabilistic reasoning**
- ✅ **Loop detection and avoidance** to prevent infinite traversal
- ✅ Interactive UI to visualize:
  - Agent's actions and decisions
  - Internal knowledge base
  - Logical reasoning process

---

## Project Structure
/WumpusWorld/
├── environments/ # Pre-defined map files
├── src/
│ ├── logic/ # Logical representation & inference modules
│ ├── agent/ # Agent implementation
│ ├── ui/ # User interface code
│ └── main.py # Entry point of the application
├── requirements.txt # Dependencies (if any)
└── README.md # Project documentation


---

## 🛠 How to Run

1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-username/wumpus-agent.git
   cd wumpus-agent
2. **Install Dependencies**
    pip install -r requirements.txt

3. **Run the Program**
    python src/main.py

