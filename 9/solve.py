
import sys

def solve():
    filename = 'input.txt'
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    
    try:
        with open(filename, 'r') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"Error: {filename} not found")
        return

    coords = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        try:
            x, y = map(int, line.split(','))
            coords.append((x, y))
        except ValueError:
            print(f"Skipping invalid line: {line}")
            continue

    if not coords:
        print("No valid coordinates found.")
        return

    max_area = 0
    n = len(coords)

    for i in range(n):
        for j in range(i + 1, n):
            x1, y1 = coords[i]
            x2, y2 = coords[j]

            width = abs(x1 - x2) + 1
            height = abs(y1 - y2) + 1
            
            area = width * height
            if area > max_area:
                max_area = area

    print(f"Max area: {max_area}")

if __name__ == "__main__":
    solve()
