import numpy as np
import matplotlib.pyplot as plt
from itertools import permutations, product


def create_empty_grid(rows, cols):
    return np.full((rows, cols), 'E')


def can_place(grid, row, col, shape):
    """Check if the shape can be placed at the given position."""
    return row + shape[0] <= grid.shape[0] and col + shape[1] <= grid.shape[1]


def place_shape(grid, row, col, shape, color):
    """Place a shape at the given position on the grid."""
    grid_copy = grid.copy()
    grid_copy[row:row + shape[0], col:col + shape[1]] = color
    return grid_copy


def is_shape_visible(grid, color):
    """Check if any part of the shape with the given color is visible."""
    return color in grid


def normalize_pattern(grid):
    """Normalize the grid pattern to remove color differences."""
    norm_grid = grid.copy()
    norm_grid[norm_grid == "R"] = "X"
    norm_grid[norm_grid == "G"] = "Y"
    return ''.join(norm_grid.flatten())


def visualize_grid(grid, pattern_num):
    """Visualize the grid with red and green shapes"""
    # Create RGB grid with proper color mapping
    rgb_grid = np.zeros((grid.shape[0], grid.shape[1], 3))
    
    # Explicitly set colors for each cell
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            if grid[i, j] == 'R':  # Red for first shape
                rgb_grid[i, j] = [1.0, 0.0, 0.0]
            elif grid[i, j] == 'G':  # Green for second shape
                rgb_grid[i, j] = [0.0, 1.0, 0.0]
            else:  # White for empty space
                rgb_grid[i, j] = [1.0, 1.0, 1.0]

    # Create figure and axis with larger size
    fig, ax = plt.subplots(figsize=(5, 4))
    ax.imshow(rgb_grid, aspect='equal')

    # Draw grid lines with increased visibility
    ax.set_xticks(np.arange(-0.5, grid.shape[1], 1))
    ax.set_yticks(np.arange(-0.5, grid.shape[0], 1))
    ax.grid(color='black', linewidth=2)
    
    # Remove tick labels
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    
    # Add text labels to cells for better visibility
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            text_color = 'black' if grid[i, j] == 'E' else 'white'
            ax.text(j, i, grid[i, j], ha='center', va='center', 
                   color=text_color, fontsize=14, fontweight='bold')

    ax.set_title(f"Pattern {pattern_num + 1}")
    plt.tight_layout()
    plt.show()


def shape_orientations(shape):
    """Return the possible orientations of a shape (square or rectangle)."""
    if shape[0] != shape[1]:  # Rectangle
        return [shape, (shape[1], shape[0])]  # Return both orientations (horizontal and vertical)
    return [shape]  # Square has only one orientation


def generate_patterns(grid_size, shape1, shape2):
    rows, cols = grid_size
    unique_patterns = {}

    # Check all permutations of shapes
    for shape_order in permutations([(shape1, 'R'), (shape2, 'G')]):
        grids_to_process = [create_empty_grid(rows, cols)]

        for shape, color in shape_order:
            new_grids = []
            orientations = shape_orientations(shape)

            for grid in grids_to_process:
                for oriented_shape in orientations:
                    for r in range(rows):
                        for c in range(cols):
                            if can_place(grid, r, c, oriented_shape):
                                placed_grid = place_shape(grid, r, c, oriented_shape, color)
                                if is_shape_visible(placed_grid, color):
                                    new_grids.append(placed_grid)
            grids_to_process = new_grids

        for final_grid in grids_to_process:
            norm = normalize_pattern(final_grid)
            unique_patterns[norm] = final_grid

    return list(unique_patterns.values())


def validate_shapes(grid_size, shapes):
    """Ensure the shapes fit within the grid size."""
    for shape in shapes:
        if shape[0] > grid_size[0] or shape[1] > grid_size[1]:
            print(f"Error: Shape {shape} is too large for the grid {grid_size}.")
            return False
    return True


def main():
    grid_size = (3, 3)  # Customize grid size here

    # Define shapes (square and rectangle)
    shape1 = (2, 2)  # Red Square
    shape2 = (2, 2)  # Green Rectangle

    shapes = [shape1, shape2]

    # Validate shapes to ensure they fit the grid
    if not validate_shapes(grid_size, shapes):
        return

    print(f"Grid size: {grid_size}")
    print(f"Shape 1 (Red): {shape1}")
    print(f"Shape 2 (Green): {shape2}")

    patterns = generate_patterns(grid_size, shape1, shape2)

    print(f"\nTotal unique valid patterns: {len(patterns)}\n")

    for idx, grid in enumerate(patterns):
        print(f"Pattern {idx + 1}:\n{grid}\n")
        visualize_grid(grid, idx)


if __name__ == "__main__":
    main()
