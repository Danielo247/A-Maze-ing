# A-Maze-ing

*This project has been created as part of the 42 curriculum by danfranc, jdel-cer.*

---

## Description

**A-Maze-ing** is a maze generator and solver developed in Python 3.10+.  
It reads a configuration file to generate perfect mazes (a single path between any two points), exports them in hexadecimal format, and computes the shortest path between entry and exit.

The maze is generated using the Recursive Backtracker algorithm and solved using Breadth-First Search (BFS).

---

## Instructions

### Requirements

- Python 3.10+

### Execution

```bash
python3 a_maze_ing.py <config_file>
```

Example:

```bash
python3 a_maze_ing.py config.txt
```

Or:

```bash
make run
```

---

## Configuration File Structure

The configuration file must contain:

```
WIDTH=<int>
HEIGHT=<int>
ENTRY=x,y
EXIT=x,y
OUTPUT_FILE=<filename>
PERFECT=true|false
```

---

## Maze Generation Algorithm

### Recursive Backtracker (Depth-First Search)

The maze is generated using a randomized Depth-First Search (DFS) with backtracking:

1. Start from an initial cell.
2. Randomly choose an unvisited neighbor.
3. Remove the wall between the current cell and the chosen neighbor.
4. Continue until all cells are visited.

### Why this algorithm

- Produces perfect mazes.
- Simple and efficient to implement.
- Ensures full connectivity.

---

## Reusable Code

The `MazeGenerator` class is reusable and modular:

- Supports arbitrary dimensions.
- Can generate perfect mazes.
- Includes solving functionality.
- Can be extended with additional algorithms.

---

## Project Management

### Team Roles

- **danfranc** — Maze generation implementation.
- **jdel-cer** — Visualization/graphics, interactive display of the maze.

### Planning and Evolution

Initial plan:
- Implement maze generation.
- Implement solver.
- Add configuration parsing.
- Add file export.

Evolution:
- Refactored grid handling.
- Improved type annotations.
- Integrated pattern overlay.
- Improved error handling.

### What Worked Well

- Clear separation between generation and solving.
- Modular class design.

### What Could Be Improved

- Add automated testing.
- Improve scalability for larger mazes.

### Tools Used

- Python 3.10
- flake8
- mypy
- Git

---

### AI Usage

AI tools were used for documentation structuring, minor refactoring suggestions, and grammar correction.
All core logic and algorithm implementation were developed by the team.
