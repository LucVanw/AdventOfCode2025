
import sys

def solve(input_file):
    with open(input_file, 'r') as f:
        lines = [line.rstrip('\n') for line in f.readlines()]

    if not lines:
        print("No input lines.")
        return

    # Ensure all lines are padded to the same length with spaces
    max_len = max(len(line) for line in lines)
    lines = [line.ljust(max_len) for line in lines]

    num_rows = len(lines)
    num_cols = max_len

    # Identify separator columns (columns that are purely spaces)
    # A column is a separator if lines[row][col] is ' ' for all row
    separator_cols = []
    for col in range(num_cols):
        is_sep = True
        for row in range(num_rows):
            if lines[row][col] != ' ':
                is_sep = False
                break
        if is_sep:
            separator_cols.append(col)

    # Use separators to define blocks
    # Blocks are [start_col, end_col) ranges
    problem_ranges = []
    current_start = 0
    
    # Add a virtual separator at the end to close the last block
    separators_list = separator_cols + [num_cols]
    
    for sep in separators_list:
        if sep > current_start:
            # We found a block of non-space content
            problem_ranges.append((current_start, sep))
        current_start = sep + 1

    grand_total = 0

    print(f"Found {len(problem_ranges)} problems.")

    for idx, (start, end) in enumerate(problem_ranges):
        numbers = []
        operator = None
        
        # The last line (index num_rows - 1) contains the operator
        op_char = lines[num_rows - 1][start:end].strip()
        
        # Part 2: Read numbers vertically, right to left
        # Columns range from end-1 down to start
        for c in range(end - 1, start - 1, -1):
            digit_str = ""
            for r in range(num_rows - 1):
                char = lines[r][c]
                if char.strip():
                     digit_str += char
            
            if digit_str:
                numbers.append(int(digit_str))
        
        if not op_char:
             print(f"Problem {idx}: No operator found in range {start}-{end}")
             continue
             
        operator = op_char
        
        result = 0
        if operator == "+":
            result = sum(numbers)
        elif operator == "*":
            result = 1
            for n in numbers:
                result *= n
        else:
            print(f"Problem {idx}: Unknown operator '{operator}'")

        # print(f"Problem {idx}: {numbers} {operator} = {result}")
        grand_total += result

    print(f"Grand Total: {grand_total}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        solve(sys.argv[1])
    else:
        solve("input.txt")
