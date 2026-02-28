"""
ASCII terminal-based maze visualization.
Alternative to graphical display using terminal rendering.
"""

from typing import List, Tuple, Set


class TerminalVisualizer:
    """
    Terminal-based maze visualizer using ASCII art.
    """

    def __init__(self, width: int, height: int, cell_char_width: int = 2) -> None:
        """
        Initialize the terminal visualizer.

        Args:
            width: Maze width in cells
            height: Maze height in cells
            cell_char_width: Width of each cell in characters
        """
        self.maze_width = width
        self.maze_height = height
        self.cell_char_width = cell_char_width

        self.grid: List[List[int]] = []
        self.pattern: List[Tuple[int, int]] = []
        self.entry: Tuple[int, int] = (0, 0)
        self.exit: Tuple[int, int] = (0, 0)
        self.solution_path: str = ""

    def set_maze_data(
        self,
        grid: List[List[int]],
        pattern: List[Tuple[int, int]],
        entry: Tuple[int, int],
        exit_pos: Tuple[int, int],
        solution: str
    ) -> None:
        """
        Set the maze data to be visualized.

        Args:
            grid: The maze grid with wall data
            pattern: List of cells forming the 42 pattern
            entry: Entry coordinates
            exit_pos: Exit coordinates
            solution: Solution path as string of directions
        """
        self.grid = grid
        self.pattern = pattern
        self.entry = entry
        self.exit = exit_pos
        self.solution_path = solution

    def _has_wall(self, cell_value: int, direction: str) -> bool:
        """
        Check if a cell has a wall in a given direction.

        Args:
            cell_value: The hexadecimal cell value
            direction: 'N', 'E', 'S', or 'W'

        Returns:
            True if wall exists, False otherwise
        """
        wall_bits = {'N': 1, 'E': 2, 'S': 4, 'W': 8}
        return (cell_value & wall_bits.get(direction, 0)) != 0

    def _get_solution_cells(self) -> Set[Tuple[int, int]]:
        """
        Get all cells that are part of the solution path.

        Returns:
            Set of tuples representing solution path cells
        """
        cells: Set[Tuple[int, int]] = {self.entry}
        current_x, current_y = self.entry

        direction_map = {
            'N': (0, -1),
            'E': (1, 0),
            'S': (0, 1),
            'W': (-1, 0)
        }

        for direction in self.solution_path:
            if direction in direction_map:
                dx, dy = direction_map[direction]
                current_x += dx
                current_y += dy
                cells.add((current_x, current_y))

        return cells

    def display(self, show_solution: bool = True) -> None:
        """
        Display the maze in the terminal using ASCII art.

        Args:
            show_solution: Whether to show the solution path
        """
        solution_cells = self._get_solution_cells() if show_solution else set()

        # Create output grid
        output_height = (self.maze_height * 2) + 1
        output_width = (self.maze_width * self.cell_char_width) + 1
        output: List[List[str]] = [
            ['█' for _ in range(output_width)]
            for _ in range(output_height)
        ]

        # Fill in cells
        for y in range(self.maze_height):
            for x in range(self.maze_width):
                cell_value = self.grid[y][x]

                # Cell visual position
                char_y = y * 2 + 1
                char_x = x * self.cell_char_width

                # Determine cell character
                if (x, y) in self.pattern:
                    cell_char = '4'  # Pattern indicator
                elif (x, y) == self.entry:
                    cell_char = 'S'  # Start
                elif (x, y) == self.exit:
                    cell_char = 'E'  # End
                elif (x, y) in solution_cells:
                    cell_char = '·'  # Solution path
                else:
                    cell_char = ' '  # Empty

                # Draw cell (fill entire cell area)
                for i in range(self.cell_char_width):
                    if char_x + i < output_width:
                        output[char_y][char_x + i] = cell_char

                # Remove walls based on cell value
                # North wall - remove if no wall
                if not self._has_wall(cell_value, 'N') and char_y > 0:
                    for i in range(self.cell_char_width):
                        if char_x + i < output_width:
                            output[char_y - 1][char_x + i] = ' '

                # South wall - remove if no wall
                if not self._has_wall(cell_value, 'S') and char_y + 1 < output_height:
                    for i in range(self.cell_char_width):
                        if char_x + i < output_width:
                            output[char_y + 1][char_x + i] = ' '

                # West wall - remove if no wall
                if not self._has_wall(cell_value, 'W') and char_x > 0:
                    output[char_y][char_x - 1] = ' '

                # East wall - remove if no wall
                if not self._has_wall(cell_value, 'E') and char_x + self.cell_char_width < output_width:
                    output[char_y][char_x + self.cell_char_width] = ' '

        # Print maze with padding
        print("\n" + "=" * (output_width + 4))
        print(" " * ((output_width - 19) // 2) + "Maze Visualization")
        print("=" * (output_width + 4) + "\n")

        for row in output:
            print('  ' + ''.join(row))

        print("\n" + "=" * (output_width + 4))
        print("Legend:")
        print("  S = Start (Entry point)")
        print("  E = End (Exit point)")
        print("  4 = 42 Pattern")
        print("  · = Solution Path" if show_solution else "  (Solution path hidden)")
        print("  █ = Wall (Closed passage)")
        print("  (space) = Open passage")
        print("=" * (output_width + 4) + "\n")
