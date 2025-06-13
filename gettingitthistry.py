import numpy as np
import matplotlib.pyplot as plt
from itertools import permutations

def create_empty_grid(rows, cols):
    return np.full((rows, cols), 'E')

def can_place(grid, row, col, shape):
    return row + shape[0] <= grid.shape[0] and col + shape[1] <= grid.shape[1]

def place_shape(grid, row, col, shape, color):
    grid_copy = grid.copy()
    grid_copy[row:row + shape[0], col:col + shape[1]] = color
    return grid_copy

def is_shape_visible(grid, color):
    return color in grid

def visualize_grid(grid, pattern_num):
    rgb_grid = np.zeros((grid.shape[0], grid.shape[1], 3))

    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            if grid[i, j] == 'R':
                rgb_grid[i, j] = [1.0, 0.0, 0.0]
            elif grid[i, j] == 'G':
                rgb_grid[i, j] = [0.0, 1.0, 0.0]
            elif grid[i, j] == 'B':
                rgb_grid[i, j] = [0.0, 0.0, 1.0]
            else:
                rgb_grid[i, j] = [1.0, 1.0, 1.0]

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.imshow(rgb_grid, aspect='equal')
    ax.set_xticks(np.arange(-0.5, grid.shape[1], 1))
    ax.set_yticks(np.arange(-0.5, grid.shape[0], 1))
    ax.grid(color='black', linewidth=2)
    ax.set_xticklabels([])
    ax.set_yticklabels([])

    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            text_color = 'black' if grid[i, j] == 'E' else 'white'
            ax.text(j, i, grid[i, j], ha='center', va='center',
                    color=text_color, fontsize=14, fontweight='bold')

    ax.set_title(f"Pattern {pattern_num + 1}")
    plt.tight_layout()
    plt.show()

def shape_orientations(shape):
    if shape[0] != shape[1]:
        return [shape, (shape[1], shape[0])]
    return [shape]

def grid_to_string(grid):
    """Convert grid to a single string representation."""
    return ''.join(grid.flatten())

def generate_patterns(grid_size, shapes):
    rows, cols = grid_size
    all_patterns = []  # Stores ALL patterns in order
    seen_patterns = set()  # Checks for duplicates

    shape_orders = permutations([('R', shapes[0]), ('G', shapes[1]), ('B', shapes[2])])

    for shape_order in shape_orders:
        grids_to_process = [create_empty_grid(rows, cols)]

        for color, shape in shape_order:
            new_grids = []
            orientations = shape_orientations(shape)

            for grid in grids_to_process:
                for oriented_shape in orientations:
                    for r in range(rows):
                        for c in range(cols):
                            if can_place(grid, r, c, oriented_shape):
                                placed_grid = place_shape(grid, r, c, oriented_shape, color)
                                new_grids.append(placed_grid)

            grids_to_process = new_grids

        for final_grid in grids_to_process:
            grid_str = grid_to_string(final_grid)
            is_duplicate = grid_str in seen_patterns
            seen_patterns.add(grid_str)
            # Store both the grid and whether it's duplicate
            all_patterns.append((final_grid, is_duplicate))

    return all_patterns




def validate_shapes(grid_size, shapes):
    for shape in shapes:
        if shape[0] > grid_size[0] or shape[1] > grid_size[1]:
            print(f"Error: Shape {shape} is too large for the grid {grid_size}.")
            return False
    return True

def main():
    grid_size = (3, 9)

    shape1 = (3, 3)  # Red shape (Square)
    shape2 = (2, 5)  # Green shape (Rectangle)
    shape3 = (1, 9)  # Blue shape (Rectangle)

    shapes = [shape1, shape2, shape3]

    if not validate_shapes(grid_size, shapes):
        return

    patterns = generate_patterns(grid_size, shapes)

    total_patterns = len(patterns)
    unique_patterns = sum(1 for _, is_dup in patterns if not is_dup)
    duplicates = total_patterns - unique_patterns

    print(f"\nTotal patterns generated: {total_patterns}")
    print(f"Unique patterns: {unique_patterns}")
    print(f"Duplicate patterns: {duplicates}\n")

    # Clearly show duplicates when visualizing
    for idx, (grid, is_duplicate) in enumerate(patterns):
        dup_str = " (Duplicate)" if is_duplicate else ""
        print(f"Pattern {idx + 1}{dup_str}:\n{grid}\n")
        visualize_grid(grid, idx)


if __name__ == "__main__":
    main()
