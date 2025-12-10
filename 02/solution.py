#!/usr/bin/env python3
"""
Advent of Code 2025 - Day 2: Gift Shop
Find and sum all invalid product IDs across given ranges.
An ID is invalid if it's made of a sequence of digits repeated exactly twice.
"""

def is_invalid_id(num, part=2):
    """
    Check if a number is an invalid ID.
    
    Part 1: A number is invalid if it's made of some sequence repeated exactly twice.
    Examples: 11 (1 twice), 6464 (64 twice), 123123 (123 twice)
    
    Part 2: A number is invalid if it's made of some sequence repeated at least twice.
    Examples: 12341234 (1234 two times), 123123123 (123 three times),
              1212121212 (12 five times), 1111111 (1 seven times)
    """
    s = str(num)
    length = len(s)
    
    if part == 1:
        # Part 1: Must be even length and split in half
        if length % 2 != 0:
            return False
        mid = length // 2
        first_half = s[:mid]
        second_half = s[mid:]
        return first_half == second_half
    
    else:  # part == 2
        # Part 2: Try all possible pattern lengths
        # A pattern must repeat at least twice, so max pattern length is length//2
        for pattern_len in range(1, length // 2 + 1):
            # Check if the length is divisible by pattern length
            if length % pattern_len == 0:
                pattern = s[:pattern_len]
                # Check if the entire string is this pattern repeated
                num_repeats = length // pattern_len
                if pattern * num_repeats == s:
                    return True
        return False


def find_invalid_ids_in_range(start, end, part=2):
    """Find all invalid IDs in the given range [start, end] inclusive."""
    invalid_ids = []
    for num in range(start, end + 1):
        if is_invalid_id(num, part=part):
            invalid_ids.append(num)
    return invalid_ids


def solve(input_file, part=2):
    """Solve the puzzle given the input file path."""
    # Read the input
    with open(input_file, 'r') as f:
        data = f.read().strip()
    
    # Parse the ranges
    ranges = []
    for range_str in data.split(','):
        range_str = range_str.strip()
        start, end = range_str.split('-')
        ranges.append((int(start), int(end)))
    
    # Find all invalid IDs
    all_invalid_ids = []
    for start, end in ranges:
        invalid_ids = find_invalid_ids_in_range(start, end, part=part)
        all_invalid_ids.extend(invalid_ids)
        if invalid_ids:
            print(f"{start}-{end} has {len(invalid_ids)} invalid ID(s): {invalid_ids}")
        else:
            print(f"{start}-{end} contains no invalid IDs")
    
    # Calculate the sum
    total = sum(all_invalid_ids)
    
    print(f"\nTotal sum of all invalid IDs: {total}")
    return total



if __name__ == "__main__":
    # Test with the examples from the problem
    print("=== Testing Part 1 (exactly twice) ===")
    test_cases_part1 = [
        (11, True),
        (22, True),
        (99, True),
        (1010, True),
        (1188511885, True),
        (222222, True),
        (446446, True),
        (38593859, True),
        (101, False),  # Should be valid (not invalid)
        (111, False),  # Part 1: not exactly twice
        (999, False),  # Part 1: not exactly twice
    ]
    
    for num, expected in test_cases_part1:
        result = is_invalid_id(num, part=1)
        status = "✓" if result == expected else "✗"
        print(f"{status} {num}: {result} (expected {expected})")
    
    print("\n=== Testing Part 2 (at least twice) ===")
    test_cases_part2 = [
        (11, True),       # 1 repeated 2 times
        (22, True),       # 2 repeated 2 times
        (99, True),       # 9 repeated 2 times
        (111, True),      # 1 repeated 3 times
        (999, True),      # 9 repeated 3 times
        (1010, True),     # 10 repeated 2 times
        (12341234, True), # 1234 repeated 2 times
        (123123123, True),# 123 repeated 3 times
        (1212121212, True), # 12 repeated 5 times
        (1111111, True),  # 1 repeated 7 times
        (565656, True),   # 56 repeated 3 times
        (824824824, True),# 824 repeated 3 times
        (2121212121, True), # 21 repeated 5 times
        (101, False),     # Not a repeating pattern
    ]
    
    for num, expected in test_cases_part2:
        result = is_invalid_id(num, part=2)
        status = "✓" if result == expected else "✗"
        print(f"{status} {num}: {result} (expected {expected})")
    
    print("\n=== Solving Part 1 ===")
    solve("input.txt", part=1)
    
    print("\n=== Solving Part 2 ===")
    solve("input.txt", part=2)


