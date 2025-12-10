def parse_input(filename):
    with open(filename, 'r') as f:
        lines = f.read().splitlines()

    ranges = []
    ids = []
    parsing_ranges = True

    for line in lines:
        if not line:
            parsing_ranges = False
            continue
        
        if parsing_ranges:
            start, end = map(int, line.split('-'))
            ranges.append((start, end))
        else:
            ids.append(int(line))
            
    return ranges, ids

def is_fresh(ingredient_id, ranges):
    for start, end in ranges:
        if start <= ingredient_id <= end:
            return True
    return False

def solve(filename):
    ranges, ids = parse_input(filename)
    fresh_count = 0
    
    for ingredient_id in ids:
        if is_fresh(ingredient_id, ranges):
            fresh_count += 1
            
    return fresh_count

def merge_ranges(ranges):
    if not ranges:
        return []
    
    # Sort ranges by start value
    sorted_ranges = sorted(ranges, key=lambda x: x[0])
    
    merged = []
    current_start, current_end = sorted_ranges[0]
    
    for i in range(1, len(sorted_ranges)):
        next_start, next_end = sorted_ranges[i]
        
        if next_start <= current_end + 1: # Overlapping or adjacent
            current_end = max(current_end, next_end)
        else:
            merged.append((current_start, current_end))
            current_start, current_end = next_start, next_end
            
    merged.append((current_start, current_end))
    return merged

def solve_part2(filename):
    ranges, _ = parse_input(filename)
    merged_ranges = merge_ranges(ranges)
    
    total_fresh = 0
    for start, end in merged_ranges:
        total_fresh += (end - start + 1)
        
    return total_fresh

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = 'Input.txt'
        
    result_part1 = solve(filename)
    print(f"Part 1 - Number of fresh ingredients: {result_part1}")
    
    result_part2 = solve_part2(filename)
    print(f"Part 2 - Total fresh ingredient IDs: {result_part2}")
