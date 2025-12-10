import sys

def solve(input_file):
    try:
        with open(input_file, 'r') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"Error: File {input_file} not found.")
        return

    dial_position = 50
    part1_zero_count = 0
    part2_zero_count = 0

    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        direction = line[0]
        distance = int(line[1:])

        step = -1 if direction == 'L' else 1
        
        for _ in range(distance):
            dial_position = (dial_position + step) % 100
            if dial_position == 0:
                part2_zero_count += 1
        
        if dial_position == 0:
            part1_zero_count += 1

    print(f"Part 1 Password: {part1_zero_count}")
    print(f"Part 2 Password: {part2_zero_count}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    else:
        input_file = "input.txt"
    
    solve(input_file)
