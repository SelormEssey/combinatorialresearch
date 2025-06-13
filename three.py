import numpy as np
from itertools import permutations
import hashlib

# ---------- helpers ----------------------------------------------------------
def create_empty_grid(rows, cols):
    return np.full((rows, cols), 'E')

def can_place(grid, row, col, shape):
    return row + shape[0] <= grid.shape[0] and col + shape[1] <= grid.shape[1]

def place_shape(grid, row, col, shape, color):
    g = grid.copy()
    g[row:row + shape[0], col:col + shape[1]] = color
    return g

def shape_orientations(shape):
    return [shape, (shape[1], shape[0])] if shape[0] != shape[1] else [shape]

# *** fixed hashing function ***
def grid_hash(grid: np.ndarray) -> str:
    """Return a reliable hash that captures the exact layout of the grid."""
    # Convert grid to a binary representation then hash it
    flattened = ''.join(grid.flatten())
    # Use a proper cryptographic hash to avoid collisions
    return hashlib.md5(flattened.encode('utf-8')).hexdigest()
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------

def generate_patterns(grid_size, shapes):
    rows, cols = grid_size
    patterns           = []           # every pattern we create (including dups)
    seen               = {}           # hash -> first index
    duplicate_patterns = []           # (dup_index, original_index)

    orders = list(permutations(range(3)))   # six permutations of (0,1,2)

    for order in orders:
        grids = [create_empty_grid(rows, cols)]

        for idx in order:
            shape, color = shapes[idx]
            new_grids = []
            for grid in grids:
                for oriented in shape_orientations(shape):
                    for r in range(rows):
                        for c in range(cols):
                            if can_place(grid, r, c, oriented):
                                new_grids.append(
                                    place_shape(grid, r, c, oriented, color)
                                )
            grids = new_grids

        # de‑dup while we append to the master list
        for g in grids:
            h = grid_hash(g)
            if h in seen:
                duplicate_patterns.append((len(patterns), seen[h]))
            else:
                seen[h] = len(patterns)
            patterns.append(g)

    return patterns, duplicate_patterns

# ---------- driver -----------------------------------------------------------
def main():
    grid_size = (3, 9)
    shapes = [((3, 3), 'R'),   # red square
              ((2, 5), 'G'),   # green rectangle
              ((1, 9), 'B')]   # blue rectangle

    patterns, dups = generate_patterns(grid_size, shapes)

    print(f"Total patterns generated: {len(patterns)}")
    print(f"Total unique patterns : {len(patterns) - len(dups)}")
    print(f"Total duplicate pairs : {len(dups)}")

    if dups:
        print("\nDuplicates (new_index, original_index):")
        for new_i, first_i in dups:
            print(f"{new_i:5d}  <‑‑ duplicate of  {first_i}")

if __name__ == "__main__":
    main()