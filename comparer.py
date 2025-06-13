import numpy as np
import re, ast

def normalize_with_exact_colors(grid):
    return ''.join(grid.flatten())

def load_patterns_from_file(filename="patterns2.txt"):
    with open(filename, 'r') as f:
        text = f.read()

    # Split into blocks after each "Pattern X:"
    blocks = re.split(r'Pattern \d+:\s*\n', text)[1:]
    patterns = []
    for block in blocks:
        rows = re.findall(r"\[.*?\]", block)
        grid = []
        for row in rows:
            row_py = row.replace("'", '"')
            row_py = re.sub(r'" +(?=")', '", ', row_py)
            grid.append(ast.literal_eval(row_py))
        patterns.append(np.array(grid))
    return patterns

def dedupe_patterns(patterns):
    patterns_dict = {}
    kept = []
    for idx, grid in enumerate(patterns, 1):
        key = normalize_with_exact_colors(grid)
        if key not in patterns_dict:
            patterns_dict[key] = grid
            kept.append((idx, grid))
            print(f"✅ Pattern {idx} added")
        else:
            print(f"❌ Pattern {idx} is a duplicate and was skipped.")
    print(f"\nSummary: {len(patterns)} total, {len(kept)} unique, {len(patterns)-len(kept)} duplicates skipped")
    return kept

if __name__ == "__main__":
    patterns = load_patterns_from_file("patterns2.txt")
    kept = dedupe_patterns(patterns)
