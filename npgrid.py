import numpy as np
import matplotlib.pyplot as plt
from itertools import permutations

# Create and manage a 2D grid
def create_empty_grid(rows, cols):
    return np.full((rows, cols), 'E')

def can_place(grid, row, col, shape):
    """Check if a shape fits within the grid boundaries."""
    return row + shape[0] <= grid.shape[0] and col + shape[1] <= grid.shape[1]

def place_shape(grid, row, col, shape, color):
    """Return a new grid with the shape placed at (row, col)."""
    grid_copy = grid.copy()
    grid_copy[row:row + shape[0], col:col + shape[1]] = color
    return grid_copy

# Ensure each shape remains at least partly visible
def is_shape_visible(grid, color):
    return np.any(grid == color)

# Generate all patterns (no duplicate filtering)
def generate_patterns(grid_size, shapes):
    """Generate all patterns without duplicate filtering."""
    rows, cols = grid_size
    all_patterns = []

    for shape_order in permutations(shapes, len(shapes)):
        grids_to_process = [create_empty_grid(rows, cols)]
        for (shape, color) in shape_order:
            new_grids = []
            orientations = [(shape[0], shape[1])]
            if shape[0] != shape[1]:
                orientations.append((shape[1], shape[0]))

            for grid in grids_to_process:
                for oriented in orientations:
                    for r in range(rows):
                        for c in range(cols):
                            if can_place(grid, r, c, oriented):
                                placed = place_shape(grid, r, c, oriented, color)
                                if is_shape_visible(placed, color):
                                    new_grids.append(placed)
            grids_to_process = new_grids

        all_patterns.extend(grids_to_process)

    return all_patterns

# Validate that shapes fit the grid
def validate_shapes(grid_size, shapes):
    for shape, _ in shapes:
        if shape[0] > grid_size[0] or shape[1] > grid_size[1]:
            print(f"Error: Shape {shape} too large for grid {grid_size}.")
            return False
    return True

# Save patterns to a text file, assigning each to a NumPy array
def save_patterns_to_file(patterns, filename="patterns2.txt"):
    with open(filename, 'w') as f:
        for idx, grid in enumerate(patterns, start=1):
            f.write(f"grid{idx} = np.array([\n")
            for row in grid:
                row_str = ", ".join(f"'{c}'" for c in row)
                f.write(f"    [{row_str}],\n")
            f.write("])\n\n")
    print(f"Saved {len(patterns)} patterns to '{filename}'")

# Simple visualization of a few patterns
def visualize_grid(grid, idx):
    rgb = np.ones((*grid.shape, 3))
    mapping = {'R': [1,0,0], 'G': [0,1,0], 'B': [0,0,1], 'E': [1,1,1]}
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            rgb[i,j] = mapping[grid[i,j]]
    plt.figure(figsize=(6,3))
    plt.imshow(rgb)
    plt.xticks([])
    plt.yticks([])
    plt.title(f"Pattern {idx+1}")
    plt.show()

# Entry point
def main():
    grid_size = (3, 9)
    shapes = [((3,3),'R'), ((2,5),'G'), ((1,9),'B')]

    if not validate_shapes(grid_size, shapes):
        return

    patterns = generate_patterns(grid_size, shapes)
    print(f"\nTotal patterns (duplicates included): {len(patterns)}\n")

    save_patterns_to_file(patterns, "patterns2.txt")

    # Optionally visualize first few patterns
    for idx, pat in enumerate(patterns[:20]):
        visualize_grid(pat, idx)

if __name__ == '__main__':
    main()
