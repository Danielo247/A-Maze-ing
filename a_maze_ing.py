import sys
from typing import Dict
from generator import MazeGenerator


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
    exit = tuple(exitlist)

    maze = MazeGenerator(width, height, is_perfect=perfect)
    maze.add_pattern()
    maze.generate()
    solution = maze.solve(entry, exit)
    maze.save_to_file("maze.txt", entry, exit, solution)


if __name__ == "__main__":
    main()
