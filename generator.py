from typing import List, Tuple, Optional, Dict
import random


class MazeGenerator:
    """
    A class to generate random mazes with specific constraints.
    """
    def __init__(
        self,
        width: int,
        height: int,
        seed: Optional[int] = None,
        is_perfect: bool = True
    ) -> None:
        """
        Initialize the maze generator with dimensions and settings.
        """
        self.width: int = width
        self.height: int = height
        self.is_perfect: bool = is_perfect
        self.pattern: List[Tuple[int, int]] = []

        if seed is not None:
            random.seed(seed)

        self.grid = []
        for y in range(height):
            row = []
            for x in range(width):
                row.append(15)
            self.grid.append(row)

        self.directions: Dict[str, Tuple[int, int, int]] = {
            'N': (0, -1, 1),
            'E': (1, 0, 2),
            'S': (0, 1, 4),
            'W': (-1, 0, 8)
        }
        self.opposite: Dict[int, int] = {1: 4, 2: 8, 4: 1, 8: 2}

    def add_pattern(self) -> None:
        """Overlay a visible 42 pattern."""
        pattern = [
            "X.X.XXX",
            "X.X...X",
            "XXX.XXX",
            "..X.X..",
            "..X.XXX"
        ]
        p_width = 7
        p_heigth = 5

        start_x = (self.width - 7) // 2
        start_y = (self.height - 5) // 2

        for y in range(p_heigth):
            actual_row = pattern[y]
            for x in range(p_width):
                caracter = actual_row[x]
                if caracter == 'X':
                    tx = start_x + x
                    ty = start_y + y
                    if 0 <= tx < self.width and 0 <= ty < self.height:
                        self.pattern.append((tx, ty))

    def generate(self) -> None:
        """
        Generate the maze using the Recursive Backtracker algorithm.
        """
        stack = [(0, 0)]
        visited = [(0, 0)] + self.pattern

        while len(stack) > 0:

            current_x, current_y = stack[-1]
            neighbors = []

            for key in self.directions:
                direction_x, direction_y, wall_bit = self.directions[key]
                new_x, new_y = current_x + direction_x, current_y + direction_y

                if 0 <= new_x < self.width and 0 <= new_y < self.height:
                    if (new_x, new_y) not in visited:
                        neighbors.append((new_x, new_y, wall_bit))

            if len(neighbors) > 0:
                new_x, new_y, wall_break = random.choice(neighbors)
                self.grid[current_y][current_x] -= wall_break
                self.grid[new_y][new_x] -= self.opposite[wall_break]

                visited.append((new_x, new_y))
                stack.append((new_x, new_y))
            else:
                stack.pop()

        # If not perfect, break additional walls to create new paths
        if not self.is_perfect:
            self.non_perfect()

    def non_perfect(self) -> None:
        break_wall = (self.width * self.height) // 20

        for _ in range(break_wall):
            random_x = random.randint(0, self.width - 2)
            random_y = random.randint(0, self.height - 2)
            direction = random.randint(0, 1)

            if direction == 0:
                if (random_x, random_y) not in self.pattern and \
                        (random_x + 1, random_y) not in self.pattern:
                    # &2 == right wall
                    if (self.grid[random_y][random_x] & 2) != 0:
                        self.grid[random_y][random_x] -= 2
                        self.grid[random_y][random_x + 1] -= 8
            else:
                if (random_x, random_y) not in self.pattern and \
                        (random_x, random_y + 1) not in self.pattern:
                    # &4 == bottom wall
                    if (self.grid[random_y][random_x] & 4) != 0:
                        self.grid[random_y][random_x] -= 4
                        self.grid[random_y + 1][random_x] -= 1

    def solve(self, start: Tuple[int, int], end: Tuple[int, int]) -> str:
        """
        Find the shortest path between start and end coordinates using BFS.
        """
        queue = [(start, "")]
        visited = {start}

        while len(queue) > 0:
            current_position, path = queue.pop(0)
            current_x, current_y = current_position

            if current_x == end[0] and current_y == end[1]:
                return path

            for direction in self.directions:
                dx, dy, wall_bit = self.directions[direction]
                nx, ny = current_x + dx, current_y + dy

                if 0 <= nx < self.width and 0 <= ny < self.height:
                    if (nx, ny) not in visited:
                        if (self.grid[current_y][current_x] & wall_bit) == 0:
                            visited.add((nx, ny))
                            queue.append(((nx, ny), path + direction))
        return ""

    def save_to_file(
        self,
        filename: str,
        entry: Tuple[int, int],
        exit: Tuple[int, int],
        solution: str
    ) -> None:
        """
        Write the data to a text file in hexadecimal format.
        """
        with open(filename, 'w') as write:
            for y in range(self.height):
                for x in range(self.width):
                    write.write(format(self.grid[y][x], 'X'))
                write.write("\n")

            write.write("\n")
            entry_str = str(entry[0]) + "," + str(entry[1])
            write.write(entry_str + "\n")

            exit_str = str(exit[0]) + "," + str(exit[1])
            write.write(exit_str + "\n")

            write.write(solution + "\n")
