# A-Maze-ing

*This project has been created as part of the 42 curriculum by danfranc, jdel-cer.*

## Description

A-Maze-ing is a maze generator and solver developed in Python 3.10+. It generates perfect mazes using the Recursive Backtracker algorithm, solves them using BFS, and provides visual representation via graphics or terminal.

## Requirements

- Python 3.10+
- MLX library (for graphical display)

## Execution

### Basic Usage

```bash
python3 a_maze_ing.py config.txt
```

Or:

```bash
make run
```

The program will:
1. Generate the maze based on `config.txt`
2. Solve the maze
3. Save the result to the output file
4. Display the maze graphically (MLX) or in terminal (fallback)

## Configuration File

The configuration file must contain:

```
WIDTH=20
HEIGHT=15
ENTRY=0,0
EXIT=19,14
OUTPUT_FILE=maze.txt
PERFECT=True
```

- `WIDTH` and `HEIGHT`: Maze dimensions (in cells)
- `ENTRY` and `EXIT`: Entry and exit coordinates (x,y)
- `OUTPUT_FILE`: Output filename for the maze data
- `PERFECT`: Set to True for perfect mazes (single path), False for multiple paths

## Output File Format

The output file contains:
- Maze grid in hexadecimal format (1 hex digit per cell, encoding wall configuration)
- Entry coordinates
- Exit coordinates
- Solution path (sequence of directions: N/E/S/W)

Example format:
```
D3D13951555395153953
D3C53C543C3BC569696A
...
0,0
19,14
ESESWWSEEESENESENNNENEEEESWSWSEEESWWWSWWSEESSSSWSEENESEESWWS
```

## Interactive Display

### Graphical Mode (MLX)
- Press `S` to toggle solution visibility
- Press `C` to change wall colors
- Press `ESC` to exit

### Terminal Mode
- Shows ASCII representation of the maze
- Displays solution path automatically
