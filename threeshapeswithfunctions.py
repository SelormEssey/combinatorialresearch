import numpy as np
import matplotlib.pyplot as plt
from itertools import permutations
import pandas as pd

def create_empty_grid(rows, cols):
    return np.full((rows, cols), 'E')

def can_place(grid, row, col, shape):
    return row + shape[0] <= grid.shape[0] and col + shape[1] <= grid.shape[1]

def place_shape(grid, row, col, shape, color):
    grid_copy = grid.copy()
    grid_copy[row:row + shape[0], col:col + shape[1]] = color
    return grid_copy

def shape_orientations(shape):
    return [shape, (shape[1], shape[0])] if shape[0] != shape[1] else [shape]

def grids_are_equal(g1, g2):
    return np.array_equal(g1, g2)

def generate_patterns(grid_size, shapes):
    rows, cols = grid_size
    patterns = []
    duplicate_patterns = []

    permutations_to_process = [
        [0, 1, 2],
        [0, 2, 1],
        [1, 0, 2],
        [1, 2, 0],
        [2, 0, 1],
        [2, 1, 0],
    ]

    for order in permutations_to_process:
        grids_to_process = [create_empty_grid(rows, cols)]

        for idx in order:
            shape, color = shapes[idx]
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

        for grid in grids_to_process:
            is_duplicate = False
            for i, existing in enumerate(patterns):
                if grids_are_equal(grid, existing):
                    duplicate_patterns.append((len(patterns), i))
                    is_duplicate = True
                    break
            if not is_duplicate:
                patterns.append(grid)

    return patterns, duplicate_patterns

def main():
    grid_size = (3, 9)
    shape1 = (3, 3)  # Red Square
    shape2 = (2, 5)  # Green Rectangle
    shape3 = (1, 9)  # Blue Rectangle
    shapes = [(shape1, 'R'), (shape2, 'G'), (shape3, 'B')]

    patterns, duplicate_patterns = generate_patterns(grid_size, shapes)

    print(f"Total patterns generated: {len(patterns) + len(duplicate_patterns)}")
    print(f"Total unique patterns: {len(patterns)}")
    print(f"Total duplicate patterns: {len(duplicate_patterns)}")

    # Save duplicates to CSV
    df = pd.DataFrame(duplicate_patterns, columns=["Duplicate Index", "Original Index"])
    df.to_csv("duplicate_patterns.csv", index=False)
    print("Duplicate info saved to 'duplicate_patterns.csv'")

if __name__ == "__main__":
    main()
