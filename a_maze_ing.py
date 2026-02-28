import sys
from typing import Dict
from generator import MazeGenerator
from visualizer import MazeVisualizer
from terminal_visualizer import TerminalVisualizer


def load_config(file: str) -> Dict[str, str]:
    config_dict: Dict[str, str] = {}

    try:
        with open(file, "r") as config:
            for line in config:
                if not line or line.startswith("#"):
                    continue
                if "=" in line:
                    key, value = line.split("=", 1)
                    config_dict[key.strip()] = value.strip()

        required = ['WIDTH', 'HEIGHT', 'ENTRY',
                    'EXIT', 'OUTPUT_FILE', 'PERFECT']

        for x in required:
            if x not in config_dict:
                print(f"Missing: {x} in config.txt")
                exit(1)

    except FileNotFoundError as e:
        print(f"File error: {e}.")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)

    return config_dict


def main() -> None:

    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py <config_file>")
        sys.exit(1)

    config = load_config(sys.argv[1])

    entrylist = []
    exitlist = []
    width = int(config["WIDTH"])
    height = int(config["HEIGHT"])
    perfect = config["PERFECT"].lower() == "true"

    for x in config["ENTRY"].split(","):
        entrylist.append(int(x))
    entry = tuple(entrylist)

    for x in config["EXIT"].split(","):
        exitlist.append(int(x))
    exit_pos = tuple(exitlist)

    # Create visualizer once - larger cell size for better visibility
    visualizer = MazeVisualizer(width, height, cell_size=40)
    
    def generate_new_maze() -> None:
        """Generate a new maze and update the visualizer."""
        maze = MazeGenerator(width, height, is_perfect=perfect)
        maze.add_pattern()
        maze.generate()
        solution = maze.solve(entry, exit_pos)
        maze.save_to_file("maze.txt", entry, exit_pos, solution)
        
        # Update visualizer with new maze data
        visualizer.set_maze_data(maze.grid, maze.pattern, entry, exit_pos, solution)
        visualizer.update_display()

    def display_maze() -> None:
        """Generate and display the maze."""
        generate_new_maze()
        
        print("Maze generated and saved to maze.txt")
        
        # Display visual representation with fallback
        try:
            visualizer.display(regenerate_callback=generate_new_maze)
        except Exception as e:
            print(f"Graphical display unavailable: {e}")
            print("Showing terminal visualization instead...\n")
            terminal_viz = TerminalVisualizer(width, height)
            maze = MazeGenerator(width, height, is_perfect=perfect)
            maze.add_pattern()
            maze.generate()
            solution = maze.solve(entry, exit_pos)
            terminal_viz.set_maze_data(maze.grid, maze.pattern, entry, exit_pos, solution)
            terminal_viz.display(show_solution=True)

    display_maze()


if __name__ == "__main__":
    main()
