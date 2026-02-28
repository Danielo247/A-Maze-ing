"""
Visual representation of the maze using MLX library.
Handles rendering and user interactions for graphical display.
"""

from typing import List, Tuple, Optional, Any, Callable
import sys
import os

# Add MLX library to path
mlx_path = os.path.join(os.path.dirname(__file__), 'mlx_CLXV', 'python', 'src')
if mlx_path not in sys.path:
    sys.path.insert(0, mlx_path)

try:
    from mlx.mlx import Mlx
except ImportError as e:
    print(f"Warning: Could not import MLX: {e}")
    Mlx = None  # type: ignore


class MazeVisualizer:
    """
    A class to visualize maze using MLX graphics library.
    Handles rendering, user interactions, and maze solution display.
    """

    # Color palettes
    PALETTE_1 = {"wall": 0x000000, "name": "Black & White"}
    PALETTE_2 = {"wall": 0xFF6600, "name": "Orange & Blue"}
    PALETTE_3 = {"wall": 0xFF0066, "name": "Pink & Cyan"}

    # Other color constants (RGB)
    COLOR_PATH: int = 0xFFFFFF  # White
    COLOR_ENTRY: int = 0x00FF00  # Green
    COLOR_EXIT: int = 0xFF0000  # Red
    COLOR_SOLUTION: int = 0xFFFF00  # Yellow
    COLOR_PATTERN: int = 0xFF00FF  # Magenta
    COLOR_BACKGROUND: int = 0x1a1a1a  # Very dark gray

    def __init__(
        self,
        width: int,
        height: int,
        cell_size: int = 30
    ) -> None:
        """
        Initialize the maze visualizer.

        Args:
            width: Maze width in cells
            height: Maze height in cells
            cell_size: Size of each cell in pixels
        """
        self.maze_width = width
        self.maze_height = height
        self.cell_size = cell_size

        # Padding around the maze (in pixels)
        self.padding = 50
        
        # Window dimensions with padding
        self.maze_area_width = width * cell_size
        self.maze_area_height = height * cell_size
        
        self.window_width = self.maze_area_width + (self.padding * 2)
        self.window_height = self.maze_area_height + (self.padding * 2)

        self.grid: List[List[int]] = []
        self.pattern: List[Tuple[int, int]] = []
        self.entry: Tuple[int, int] = (0, 0)
        self.exit: Tuple[int, int] = (0, 0)
        self.solution_path: str = ""

        self.show_solution = False
        self.current_palette = 0
        self.palettes = [self.PALETTE_1, self.PALETTE_2, self.PALETTE_3]
        
        # Animation state for progressive solution display
        self.is_animating = False
        self.animation_progress = 0  # Current step in the solution path
        self.animation_frame_counter = 0  # Frame counter for speed control
        self.animation_speed = 80  # Frames between steps (lower = faster)
        
        self.mlx: Optional[Any] = None
        self.mlx_ptr: Optional[Any] = None
        self.window: Optional[Any] = None
        self.image: Optional[Any] = None
        
        # Callback for regeneration
        self.regenerate_callback: Optional[Callable[[], None]] = None

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

    def _initialize_mlx(self) -> bool:
        """
        Initialize MLX library and create window.

        Returns:
            True if initialization successful, False otherwise
        """
        try:
            if Mlx is None:
                print("Error: MLX library not available")
                return False

            self.mlx = Mlx()
            self.mlx_ptr = self.mlx.mlx_init()
            if self.mlx_ptr is None:
                print("Error: Failed to initialize MLX")
                return False

            self.window = self.mlx.mlx_new_window(
                self.mlx_ptr,
                self.window_width,
                self.window_height,
                "A-Maze-ing"
            )

            if self.window is None:
                print("Error: Failed to create MLX window")
                return False

            self.image = self.mlx.mlx_new_image(
                self.mlx_ptr,
                self.window_width,
                self.window_height
            )

            if self.image is None:
                print("Error: Failed to create MLX image")
                return False

            return True
        except Exception as e:
            print(f"Error initializing MLX: {e}")
            return False

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

    def _draw_pixel(
        self,
        x: int,
        y: int,
        color: int
    ) -> None:
        """
        Draw a single pixel on the image.

        Args:
            x: X coordinate
            y: Y coordinate
            color: Color value in hex
        """
        if not self.mlx or not self.image:
            return

        try:
            data, bits_per_pixel, size_line, _ = self.mlx.mlx_get_data_addr(
                self.image
            )

            # Ensure coordinates are within bounds
            if x < 0 or x >= self.window_width:
                return
            if y < 0 or y >= self.window_height:
                return

            if bits_per_pixel == 32:
                offset = (y * size_line) + (x * 4)
                # ARGB format (little-endian)
                data[offset + 0] = int(color & 0xFF)
                data[offset + 1] = int((color >> 8) & 0xFF)
                data[offset + 2] = int((color >> 16) & 0xFF)
                data[offset + 3] = 0xFF
        except Exception:
            pass

    def _draw_rectangle(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        color: int
    ) -> None:
        """Draw a filled rectangle."""
        for dy in range(height):
            for dx in range(width):
                self._draw_pixel(x + dx, y + dy, color)

    def _draw_cell(self, cell_x: int, cell_y: int) -> None:
        """
        Draw a single maze cell with its walls.

        Args:
            cell_x: X coordinate of the cell in the maze
            cell_y: Y coordinate of the cell in the maze
        """
        if cell_x < 0 or cell_x >= self.maze_width:
            return
        if cell_y < 0 or cell_y >= self.maze_height:
            return

        # Use padding for offsets
        x_offset = self.padding
        y_offset = self.padding

        pixel_x = x_offset + cell_x * self.cell_size
        pixel_y = y_offset + cell_y * self.cell_size

        cell_value = self.grid[cell_y][cell_x]

        # Determine cell color
        if (cell_x, cell_y) in self.pattern:
            cell_color = self.COLOR_PATTERN
        elif (cell_x, cell_y) == self.entry:
            cell_color = self.COLOR_ENTRY
        elif (cell_x, cell_y) == self.exit:
            cell_color = self.COLOR_EXIT
        elif self.show_solution:
            # Use animated solution if animating, otherwise use full solution
            if self.is_animating:
                solution_cells = self._get_animated_solution_cells()
            else:
                solution_cells = self._get_solution_cells()
            
            if (cell_x, cell_y) in solution_cells:
                cell_color = self.COLOR_SOLUTION
            else:
                cell_color = self.COLOR_PATH
        else:
            cell_color = self.COLOR_PATH

        # Draw cell background
        for dy in range(self.cell_size - 2):
            for dx in range(self.cell_size - 2):
                self._draw_pixel(pixel_x + dx, pixel_y + dy, cell_color)

        # Draw walls
        wall_color = self.palettes[self.current_palette]["wall"]
        wall_thickness = 2

        # North wall
        if self._has_wall(cell_value, 'N'):
            for i in range(self.cell_size):
                for t in range(wall_thickness):
                    if pixel_y + t < self.window_height:
                        self._draw_pixel(pixel_x + i, pixel_y + t, wall_color)

        # East wall
        if self._has_wall(cell_value, 'E'):
            for i in range(self.cell_size):
                for t in range(wall_thickness):
                    if pixel_x + self.cell_size - 1 - t >= 0:
                        self._draw_pixel(
                            pixel_x + self.cell_size - 1 - t,
                            pixel_y + i,
                            wall_color
                        )

        # South wall
        if self._has_wall(cell_value, 'S'):
            for i in range(self.cell_size):
                for t in range(wall_thickness):
                    if pixel_y + self.cell_size - 1 - t >= 0:
                        self._draw_pixel(
                            pixel_x + i,
                            pixel_y + self.cell_size - 1 - t,
                            wall_color
                        )

        # West wall
        if self._has_wall(cell_value, 'W'):
            for i in range(self.cell_size):
                for t in range(wall_thickness):
                    if pixel_x + t < self.window_width:
                        self._draw_pixel(pixel_x + t, pixel_y + i, wall_color)

    def _get_solution_cells(self) -> set:  # type: ignore
        """
        Get all cells that are part of the solution path.

        Returns:
            Set of tuples representing solution path cells
        """
        cells = {self.entry}
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

    def _get_animated_solution_cells(self) -> set:  # type: ignore
        """
        Get only the cells up to the current animation progress.

        Returns:
            Set of tuples representing the animated solution path
        """
        cells = {self.entry}
        current_x, current_y = self.entry

        direction_map = {
            'N': (0, -1),
            'E': (1, 0),
            'S': (0, 1),
            'W': (-1, 0)
        }

        # Only iterate up to the animation progress
        for i, direction in enumerate(self.solution_path):
            if i >= self.animation_progress:
                break
            if direction in direction_map:
                dx, dy = direction_map[direction]
                current_x += dx
                current_y += dy
                cells.add((current_x, current_y))

        return cells

    def _render_maze(self) -> None:
        """Render the entire maze to the image buffer."""
        # Clear maze area with background color
        for y in range(self.maze_area_height):
            for x in range(self.window_width):
                self._draw_pixel(x, y, self.COLOR_BACKGROUND)

        # Draw all cells
        for y in range(self.maze_height):
            for x in range(self.maze_width):
                self._draw_cell(x, y)

    def _render_maze_fast(self) -> None:
        """
        Fast render for animation - only updates the animated solution cells.
        Much faster than full re-render.
        """
        # Get the current animated cells
        animated_cells = self._get_animated_solution_cells()
        
        # If this is the first frame of animation, do a full render
        if self.animation_progress == 1:
            self._render_maze()
            return
        
        # Otherwise just update the newly added cell(s)
        if self.animation_progress > 0 and self.animation_progress <= len(self.solution_path):
            # Get the current position of the solution
            current_x, current_y = self.entry
            direction_map = {
                'N': (0, -1),
                'E': (1, 0),
                'S': (0, 1),
                'W': (-1, 0)
            }
            
            # Follow path to the current position
            for i in range(self.animation_progress):
                if i < len(self.solution_path):
                    direction = self.solution_path[i]
                    if direction in direction_map:
                        dx, dy = direction_map[direction]
                        current_x += dx
                        current_y += dy
            
            # Only redraw the current cell
            self._draw_cell(current_x, current_y)
            self._put_image_to_window()


    def _put_image_to_window(self) -> None:
        """Display the rendered image on the window."""
        if not self.mlx or not self.window or not self.image or not self.mlx_ptr:
            return

        try:
            self.mlx.mlx_put_image_to_window(
                self.mlx_ptr,
                self.window,
                self.image,
                0,
                0
            )
        except Exception:
            pass

    def _update_animation(self, param: object) -> int:
        """
        Update the animation progress for progressive solution display.
        
        Args:
            param: Parameter passed by MLX loop hook
            
        Returns:
            0 to continue the loop
        """
        if not self.is_animating:
            return 0

        # Always advance animation by 1 step per call for maximum speed
        self.animation_progress += 1

        # Check if animation is complete
        if self.animation_progress >= len(self.solution_path):
            self.is_animating = False
            self.animation_progress = len(self.solution_path)

        # Use fast render for animation (only updates the new cell)
        self._render_maze_fast()

        return 0

    def _key_handler(self, keycode: int, param: object) -> int:
        """
        Handle keyboard input.

        Args:
            keycode: The key code from MLX
            param: Parameter passed to the callback

        Returns:
            0 to continue, non-zero to exit
        """
        # '1' key - Regenerate maze (49)
        if keycode == 49:
            # Regenerate with clean maze (no solution shown)
            if self.regenerate_callback:
                self.regenerate_callback()
            # Reset animation state
            self.show_solution = False
            self.is_animating = False
            self.animation_progress = 0
            self.animation_frame_counter = 0
            # Render clean maze
            self._render_maze()
            self._put_image_to_window()
            return 0

        # '2' key - Start solution animation (50)
        if keycode == 50:
            # Always start animating the solution
            self.show_solution = True
            self.is_animating = True
            self.animation_progress = 0
            self.animation_frame_counter = 0
            
            # Render initial state
            self._render_maze()
            self._put_image_to_window()
            return 0

        # '3' key - Rotate colors (51)
        if keycode == 51:
            self.current_palette = (self.current_palette + 1) % len(self.palettes)
            self._render_maze()
            self._put_image_to_window()
            return 0

        # '4' key or ESC - Quit (52 or 65307)
        if keycode == 52 or keycode == 65307:
            if self.mlx and self.mlx_ptr:
                self.mlx.mlx_loop_exit(self.mlx_ptr)
            return 0

        return 0

    def display(self, regenerate_callback: Optional[Callable[[], None]] = None) -> None:
        """
        Display the maze in an MLX window.
        Handles user interactions and event loop.

        Args:
            regenerate_callback: Function to call when regenerating maze
        """
        self.regenerate_callback = regenerate_callback
        
        if not self._initialize_mlx():
            print("Error: Could not initialize graphics")
            return

        try:
            # Initial render
            self._render_maze()
            self._put_image_to_window()

            # Set up key hook and loop hook for animation
            if self.mlx and self.window and self.mlx_ptr:
                self.mlx.mlx_key_hook(self.window, self._key_handler, self)
                self.mlx.mlx_loop_hook(self.mlx_ptr, self._update_animation, self)
                self.mlx.mlx_loop(self.mlx_ptr)

        except Exception as e:
            print(f"Error during display: {e}")
        finally:
            self._cleanup()

    def update_display(self) -> None:
        """Update the display after maze data changes."""
        if self.mlx and self.window and self.image and self.mlx_ptr:
            self._render_maze()
            self._put_image_to_window()

    def _cleanup(self) -> None:
        """Clean up MLX resources."""
        if not self.mlx or not self.mlx_ptr:
            return

        try:
            if self.image:
                self.mlx.mlx_destroy_image(self.mlx_ptr, self.image)
            if self.window:
                self.mlx.mlx_destroy_window(self.mlx_ptr, self.window)
            self.mlx.mlx_release(self.mlx_ptr)
        except Exception as e:
            print(f"Error during cleanup: {e}")
