# Search Agents Implementation - Artificial Intelligence Project

[![en](https://img.shields.io/badge/lang-en-blue.svg)](https://github.com/valtimore/MazeGameIA/blob/main/README.md)
[![es](https://img.shields.io/badge/lang-es-blue.svg)](https://github.com/valtimore/MazeGameIA/blob/main/README-es.md)

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python)  
![Pygame](https://img.shields.io/badge/Pygame-2.0%2B-orange?logo=pygame)  

This project implements a game based on search agents where character 1 (Gon) must find his enemy character 2 (Neferpitou) while avoiding character 3 (Killua), who tries to intercept him using different search algorithms.

## 📋 Project Description

The project consists of a maze where two agents interact:
  
  - Gon: Uses depth-limited search to find Neferpitou
  - Killua: Mainly uses breadth-first search, but with a 40% chance switches to A* search
  - Power-up: A ramen that halves the movement cost when picked up

## 🎯 Features

  - Implementation of three search algorithms: depth-limited, breadth-first, and A*
  - Graphical interface developed with Pygame
  - Power-up system that affects movement cost
  - Probabilistic behavior for the Killua agent
  - Multiple game ending scenarios

## 📋 Prerequisites

  - Python 3.8 or higher
  - Pygame 2.0 or higher

## 🔧 Installation

Follow these steps to install and set up the project:

1. Clone the repository:
   ```bash
   git clone https://github.com/valtimore/MazeGameIA.git
   cd MazeGameIA
   ```
2. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # or
   venv\Scripts\activate  # Windows
   ```
3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## ⚙️ Run

To start the game, run:

```bash
python main.py
```

The game runs automatically. Agents move according to their search algorithms. Watch how they interact in the maze.

## Authors ✒️

* **Juan David Cataño** - [Zers04](https://github.com/Zers04)
* **Valentina Londoño** - [Valtimore](https://github.com/valtimore)

## License 📄

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
