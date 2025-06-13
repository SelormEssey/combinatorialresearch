import numpy as np
import matplotlib.pyplot as plt

def create_empty_grid(rows, cols):
    return np.full((rows, cols), 'E')

def can_place(grid, row, col, shape):
    return row + shape[0] <= grid.shape[0] and col + shape[1] <= grid.shape[1]

def place_shape(grid, row, col, shape, color):
    grid_copy = grid.copy()
    grid_copy[row:row+shape[0], col:col+shape[1]] = color
    return grid_copy

def is_shape_visible(grid, color):
    return color in grid

def normalize_pattern(grid):
    norm_grid = grid.copy()
    norm_grid[norm_grid == "R"] = "X"
    norm_grid[norm_grid == "G"] = "Y"
    return ''.join(norm_grid.flatten())

def visualize_grid(grid, pattern_num):
    """Visualize the grid with red and green shapes"""
    # Create RGB grid with proper color mapping
    rgb_grid = np.zeros((grid.shape[0], grid.shape[1], 3))
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            if grid[i, j] == 'R':  # Red for first shape
                rgb_grid[i, j] = [1, 0, 0]
            elif grid[i, j] == 'G':  # Green for second shape
                rgb_grid[i, j] = [0, 1, 0]
            else:  # White for empty space
                rgb_grid[i, j] = [1, 1, 1]

    fig, ax = plt.subplots(figsize=(4, 3))
    ax.imshow(rgb_grid, aspect='equal')

    # Draw grid lines
    ax.set_xticks(np.arange(-0.5, grid.shape[1], 1))
    ax.set_yticks(np.arange(-0.5, grid.shape[0], 1))
    ax.grid(color="black", linestyle="-", linewidth=2)
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.set_title(f"Pattern {pattern_num + 1}")

    plt.show()

def generate_patterns(grid_size, shape1, shape2, shape2_is_rectangle):
    rows, cols = grid_size
    unique_patterns = {}

    orientations_shape2 = [shape2]
    if shape2_is_rectangle and shape2[0] != shape2[1]:
        orientations_shape2.append((shape2[1], shape2[0]))  # vertical orientation

    # Place shape1 first, then shape2
    for r1 in range(rows):
        for c1 in range(cols):
            grid = create_empty_grid(rows, cols)
            if not can_place(grid, r1, c1, shape1):
                continue
            grid_shape1 = place_shape(grid, r1, c1, shape1, 'R')

            for orientation in orientations_shape2:
                for r2 in range(rows):
                    for c2 in range(cols):
                        if can_place(grid_shape1, r2, c2, orientation):
                            final_grid = place_shape(grid_shape1, r2, c2, orientation, 'G')
                            if is_shape_visible(final_grid, 'R'):
                                norm_pattern = normalize_pattern(final_grid)
                                unique_patterns[norm_pattern] = final_grid

    # Place shape2 first, then shape1
    hidden_cases_seen = set()
    for orientation in orientations_shape2:
        for r2 in range(rows):
            for c2 in range(cols):
                grid = create_empty_grid(rows, cols)
                if not can_place(grid, r2, c2, orientation):
                    continue
                grid_shape2 = place_shape(grid, r2, c2, orientation, 'G')

                for r1 in range(rows):
                    for c1 in range(cols):
                        if can_place(grid_shape2, r1, c1, shape1):
                            final_grid = place_shape(grid_shape2, r1, c1, shape1, 'R')

                            if not is_shape_visible(final_grid, 'G'):
                                norm_pattern = normalize_pattern(final_grid)
                                if norm_pattern not in hidden_cases_seen:
                                    hidden_cases_seen.add(norm_pattern)
                                    unique_patterns[norm_pattern] = final_grid
                            else:
                                norm_pattern = normalize_pattern(final_grid)
                                unique_patterns[norm_pattern] = final_grid

    return list(unique_patterns.values())

def main():
    # Customizable Input
    grid_size = (3, 3)

    # Input Shapes Here:
    shape1 = (2, 2)  # Shape 1 (always Red)
    shape2 = (2, 2)  # Shape 2 (always Green)

    # Specify if Shape 2 is a rectangle (True) or square (False)
    shape2_is_rectangle = True


    # Size validation before running
    if (shape1[0] > grid_size[0] or shape1[1] > grid_size[1] or
        shape2[0] > grid_size[0] or shape2[1] > grid_size[1]):
        print("Error: One or both shapes are too large for the given grid size.")
        return

    print(f"Grid size: {grid_size}")
    print(f"Shape 1 (Red): {shape1}")
    print(f"Shape 2 (Green): {shape2} (Rectangle: {shape2_is_rectangle})")

    patterns = generate_patterns(grid_size, shape1, shape2,shape2_is_rectangle)

    print(f"\nTotal unique valid patterns: {len(patterns)}\n")

    for idx, grid in enumerate(patterns):
        print(f"Pattern {idx + 1}:\n{grid}\n")
        visualize_grid(grid, idx)

if __name__ == "__main__":
    main()
