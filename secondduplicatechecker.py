import numpy as np
import matplotlib.pyplot as plt
from itertools import permutations, product

def create_empty_grid(rows, cols):
    return np.full((rows, cols), 'E')

def can_place(grid, r, c, shape):
    return r + shape[0] <= grid.shape[0] and c + shape[1] <= grid.shape[1]

def place_shape(grid, r, c, shape, color):
    g = grid.copy()
    g[r:r+shape[0], c:c+shape[1]] = color
    return g

def shape_orientations(shape):
    return [shape, (shape[1], shape[0])] if shape[0] != shape[1] else [shape]

def normalize_pattern(grid):
    norm = grid.copy()
    norm[norm=='R'] = 'X'
    norm[norm=='G'] = 'Y'
    norm[norm=='B'] = 'Z'
    return ''.join(norm.flatten())

def visualize_grid(grid, idx, title=""):
    """Visualize the grid with red, green, and blue shapes"""
    # Create RGB grid with proper color mapping
    rgb_grid = np.zeros((grid.shape[0], grid.shape[1], 3))
    
    # Explicitly set colors for each cell with full intensity
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            if grid[i, j] == 'R':  # Red for first shape
                rgb_grid[i, j] = [1.0, 0.0, 0.0]  # Pure red
            elif grid[i, j] == 'G':  # Green for second shape
                rgb_grid[i, j] = [0.0, 1.0, 0.0]  # Pure green
            elif grid[i, j] == 'B':  # Blue for third shape
                rgb_grid[i, j] = [0.0, 0.0, 1.0]  # Pure blue
            else:  # White for empty space
                rgb_grid[i, j] = [1.0, 1.0, 1.0]  # Pure white

    # Create figure and axis with larger size
    fig, ax = plt.subplots(figsize=(6, 4))
    
    # Display the grid with proper aspect ratio
    ax.imshow(rgb_grid, aspect='equal', interpolation='nearest')
    
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

    ax.set_title(f"{title} Pattern {idx}")
    plt.tight_layout()
    plt.show()

def generate_all_patterns(grid_size, shapes):
    """Generate every placement of three shapes (with duplicates)."""
    rows, cols = grid_size
    all_grids = []
    colors = ['R','G','B']
    for (s1,c1),(s2,c2),(s3,c3) in permutations(zip(shapes, colors), 3):
        for o1 in shape_orientations(s1):
            for r1, c1p in product(range(rows), range(cols)):
                if not can_place(create_empty_grid(rows, cols), r1, c1p, o1):
                    continue
                g1 = place_shape(create_empty_grid(rows, cols), r1, c1p, o1, c1)
                for o2 in shape_orientations(s2):
                    for r2, c2p in product(range(rows), range(cols)):
                        if not can_place(g1, r2, c2p, o2):
                            continue
                        g2 = place_shape(g1, r2, c2p, o2, c2)
                        for o3 in shape_orientations(s3):
                            for r3, c3p in product(range(rows), range(cols)):
                                if not can_place(g2, r3, c3p, o3):
                                    continue
                                g3 = place_shape(g2, r3, c3p, o3, c3)
                                all_grids.append(g3)
    return all_grids

def prune_duplicates(all_grids, visualize=False):
    """
    Keep one of each normalized layout; print & visualize all duplicate occurrences,
    but subtract each duplicate layout only once from the total.
    """
    seen_counts = {}    # norm -> total occurrences
    deleted_keys = set()
    unique = []
    deletions = 0

    for idx, g in enumerate(all_grids, 1):
        key = normalize_pattern(g)
        seen_counts[key] = seen_counts.get(key, 0) + 1

        if seen_counts[key] == 1:
            unique.append(g)  # first occurrence
        else:
            # every duplicate: report + optional visualize
            print(f"Duplicate #{idx} (occurrence {seen_counts[key]} for this key):")
            for row in g:
                print(''.join(row))
            print()
            if visualize:
                visualize_grid(g, idx, title="Duplicate")

            # subtract this key only once
            if key not in deleted_keys:
                deleted_keys.add(key)
                deletions += 1

    return unique, deletions

def validate_shapes(grid_size, shapes):
    rows, cols = grid_size
    for sh in shapes:
        if sh[0] > rows or sh[1] > cols:
            print(f"Error: shape {sh} too large for grid {grid_size}")
            return False
    return True

def main():
    grid_size = (3,9)
    shapes = [(3,3), (2,5), (1,9)]  # Red square, Green rect, Blue rect

    if not validate_shapes(grid_size, shapes):
        return

    print("Generating ALL placements (with duplicates)…")
    all_patterns = generate_all_patterns(grid_size, shapes)
    raw_total = len(all_patterns)
    print(f"  Raw total: {raw_total}")

    print("\nPruning duplicates and reporting every occurrence…")
    unique_patterns, deletions = prune_duplicates(all_patterns, visualize=True)
    final_total = len(unique_patterns)
    print(f"\nDeleted {deletions} duplicate keys  →  Final unique: {final_total}")
    print(f"Check: {raw_total} − {deletions} = {final_total}")

    # If you'd like, set visualize=True to see each duplicate grid as it's pruned.

if __name__ == "__main__":
    main()
