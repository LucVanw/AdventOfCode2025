def find_max_joltage(bank, k):
    """
    Find the maximum k-digit number by selecting k batteries from the bank.
    Uses a greedy approach: at each position, select the largest digit that
    still allows selecting enough remaining digits.
    """
    n = len(bank)
    if k > n:
        return 0
    
    result = []
    start = 0
    
    for i in range(k):
        # We need to select (k - i) more digits
        # We can consider digits from start to (n - (k - i) + 1)
        # This ensures we have enough digits left to complete the selection
        max_digit = -1
        max_pos = start
        
        for pos in range(start, n - (k - i) + 1):
            digit = int(bank[pos])
            if digit > max_digit:
                max_digit = digit
                max_pos = pos
        
        result.append(bank[max_pos])
        start = max_pos + 1
    
    return int(''.join(result))


def solve(input_file, k=2):
    with open(input_file, 'r') as f:
        banks = [line.strip() for line in f.readlines() if line.strip()]
    
    total_joltage = 0
    
    for bank in banks:
        max_joltage = find_max_joltage(bank, k)
        print(f"{bank} -> {max_joltage}")
        total_joltage += max_joltage
    
    return total_joltage


if __name__ == "__main__":
    # Test with the example for Part 1
    test_input = """987654321111111
811111111111119
234234234234278
818181911112111"""
    
    with open('test_input.txt', 'w') as f:
        f.write(test_input)
    
    print("=== Part 1 Test ===")
    test_result = solve('test_input.txt', k=2)
    print(f"\nTest total: {test_result}")
    print(f"Expected: 357\n")
    
    print("=== Part 2 Test ===")
    test_result_2 = solve('test_input.txt', k=12)
    print(f"\nTest total: {test_result_2}")
    print(f"Expected: 3121910778619\n")
    
    # Solve Part 1
    print("=== Part 1 Solution ===")
    result_part1 = solve('input.txt', k=2)
    print(f"\nTotal output joltage (Part 1): {result_part1}\n")
    
    # Solve Part 2
    print("=== Part 2 Solution ===")
    result_part2 = solve('input.txt', k=12)
    print(f"\nTotal output joltage (Part 2): {result_part2}")
