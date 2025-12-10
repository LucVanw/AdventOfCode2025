#!/usr/bin/env python3
"""
Advent of Code 2025 - Day 4: Printing Department

Count how many rolls of paper can be accessed by a forklift.
A roll can be accessed if there are fewer than 4 rolls in the 8 adjacent positions.
"""

def count_accessible_rolls(grid):
    """
    Count rolls of paper that can be accessed by a forklift.
    
    A roll (@) is accessible if it has fewer than 4 adjacent rolls (@).
    Adjacent positions are the 8 surrounding cells (including diagonals).
    """
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0
    
    # Directions for 8 adjacent cells (including diagonals)
    directions = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),           (0, 1),
        (1, -1),  (1, 0),  (1, 1)
    ]
    
    accessible_count = 0
    
    # Check each position in the grid
    for row in range(rows):
        for col in range(cols):
            # Skip if current position is not a paper roll
            if grid[row][col] != '@':
                continue
            
            # Count adjacent paper rolls
            adjacent_rolls = 0
            for dr, dc in directions:
                new_row, new_col = row + dr, col + dc
                
                # Check if the adjacent position is within bounds
                if 0 <= new_row < rows and 0 <= new_col < cols:
                    if grid[new_row][new_col] == '@':
                        adjacent_rolls += 1
            
            # If fewer than 4 adjacent rolls, this roll is accessible
            if adjacent_rolls < 4:
                accessible_count += 1
    
    return accessible_count


def count_total_removable_rolls(grid):
    """
    Count the total number of rolls that can be removed by iteratively
    removing accessible rolls until no more can be removed.
    
    Part 2: Keep removing accessible rolls (< 4 adjacent) until none remain.
    """
    # Convert grid to a mutable 2D list
    grid = [list(row) for row in grid]
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0
    
    total_removed = 0
    
    # Directions for 8 adjacent cells (including diagonals)
    directions = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),           (0, 1),
        (1, -1),  (1, 0),  (1, 1)
    ]
    
    while True:
        # Find all accessible rolls in current state
        accessible_positions = []
        
        for row in range(rows):
            for col in range(cols):
                if grid[row][col] != '@':
                    continue
                
                # Count adjacent paper rolls
                adjacent_rolls = 0
                for dr, dc in directions:
                    new_row, new_col = row + dr, col + dc
                    if 0 <= new_row < rows and 0 <= new_col < cols:
                        if grid[new_row][new_col] == '@':
                            adjacent_rolls += 1
                
                # If fewer than 4 adjacent rolls, this roll is accessible
                if adjacent_rolls < 4:
                    accessible_positions.append((row, col))
        
        # If no accessible rolls found, we're done
        if not accessible_positions:
            break
        
        # Remove all accessible rolls
        for row, col in accessible_positions:
            grid[row][col] = '.'
        
        total_removed += len(accessible_positions)
    
    return total_removed


def solve(input_file):
    """Read the input file and solve the puzzle."""
    with open(input_file, 'r') as f:
        grid = [line.rstrip('\n') for line in f]
    
    # Part 1
    result_part1 = count_accessible_rolls(grid)
    print(f"Part 1 - Number of accessible rolls: {result_part1}")
    
    # Part 2
    result_part2 = count_total_removable_rolls(grid)
    print(f"Part 2 - Total rolls removed: {result_part2}")
    
    return result_part1, result_part2


if __name__ == "__main__":
    # Test with the example
    example_grid = [
        "..@@.@@@@.",
        "@@@.@.@.@@",
        "@@@@@.@.@@",
        "@.@@@@..@.",
        "@@.@@@@.@@",
        ".@@@@@@@.@",
        ".@.@.@.@@@",
        "@.@@@.@@@@",
        ".@@@@@@@@.",
        "@.@.@@@.@."
    ]
    
    print("=" * 50)
    print("Testing with example:")
    print("=" * 50)
    
    # Part 1
    example_result_part1 = count_accessible_rolls(example_grid)
    print(f"Part 1 - Example result: {example_result_part1}")
    print(f"Part 1 - Expected: 13")
    print()
    
    # Part 2
    example_result_part2 = count_total_removable_rolls(example_grid)
    print(f"Part 2 - Example result: {example_result_part2}")
    print(f"Part 2 - Expected: 43")
    print()
    
    # Solve the actual puzzle
    print("=" * 50)
    print("Solving puzzle:")
    print("=" * 50)
    solve("input.txt")
