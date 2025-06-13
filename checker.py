from collections import Counter

# Replace this list with your actual patterns
patterns = [
    "pattern1",
    "pattern2",
    "pattern3",
    # ... add all your 1,260 patterns here
]

# Count the occurrences of each pattern
pattern_counts = Counter(patterns)

# Identify duplicates
duplicates = {pattern: count for pattern, count in pattern_counts.items() if count > 1}

# Output the results
print(f"Total duplicate patterns: {len(duplicates)}")
for pattern, count in duplicates.items():
    print(f"'{pattern}' appears {count} times")
