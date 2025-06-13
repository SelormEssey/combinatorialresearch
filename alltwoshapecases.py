import numpy as np

# Helper Functions
def create_empty_grid(rows, cols):
    return np.full((rows, cols), 'E')

def can_place(grid, row, col, shape):
    return row + shape[0] <= grid.shape[0] and col + shape[1] <= grid.shape[1]

def place_shape(grid, row, col, shape, color):
    new_grid = grid.copy()
    new_grid[row:row + shape[0], col:col + shape[1]] = color
    return new_grid

# Main Pattern Generation Function
def generate_all_patterns(grid_size, shapes_colors):
    rows, cols = grid_size
    patterns = [create_empty_grid(rows, cols)]

    for shape, color in shapes_colors:
        new_patterns = []
        shape_orientations = [shape] if shape[0] == shape[1] else [shape, (shape[1], shape[0])]
        for grid in patterns:
            for oriented_shape in shape_orientations:
                for r in range(rows):
                    for c in range(cols):
                        if can_place(grid, r, c, oriented_shape):
                            subgrid = grid[r:r + oriented_shape[0], c:c + oriented_shape[1]]
                            if np.all(subgrid == 'E'):
                                new_grid = place_shape(grid, r, c, oriented_shape, color)
                                new_patterns.append(new_grid)
        patterns = new_patterns

    return patterns

# Grid and Shapes
if __name__ == "__main__":
    grid_size = (3, 9)
    shapes_colors = [((3, 3), 'R'), ((2, 5), 'G'), ((1, 9), 'B')]

    all_patterns = generate_all_patterns(grid_size, shapes_colors)

    print(f"Total patterns generated: {len(all_patterns)}")

    # Preview a few generated patterns
    for idx, pattern in enumerate(all_patterns[:5]):
        print(f"\nPattern {idx+1}:\n{pattern}")