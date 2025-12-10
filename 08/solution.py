import sys

def solve(input_data, connection_limit):
    points = []
    for line in input_data.strip().split('\n'):
        if not line.strip(): continue
        x, y, z = map(int, line.strip().split(','))
        points.append((x, y, z))

    n = len(points)
    pairs = []
    
    # Calculate all pairwise distances
    for i in range(n):
        for j in range(i + 1, n):
            p1 = points[i]
            p2 = points[j]
            # Squared Euclidean distance is sufficient for sorting
            dist_sq = (p1[0]-p2[0])**2 + (p1[1]-p2[1])**2 + (p1[2]-p2[2])**2
            pairs.append((dist_sq, i, j))

    # Sort by distance
    pairs.sort(key=lambda x: x[0])
    
    # Union-Find / DSU
    parent = list(range(n))
    size = [1] * n

    def find(i):
        if parent[i] == i:
            return i
        parent[i] = find(parent[i])
        return parent[i]

    def union(i, j):
        root_i = find(i)
        root_j = find(j)
        if root_i != root_j:
            # Union by size
            if size[root_i] < size[root_j]:
                root_i, root_j = root_j, root_i
            parent[root_j] = root_i
            size[root_i] += size[root_j]
            return True
        return False

    # Connect top K pairs
    count_connected = 0
    for dist, u, v in pairs:
        if count_connected >= connection_limit:
            break
        union(u, v)
        count_connected += 1

    # Get circuit sizes
    circuit_sizes = []
    for i in range(n):
        if parent[i] == i:
            circuit_sizes.append(size[i])
            
    circuit_sizes.sort(reverse=True)
    
    if len(circuit_sizes) < 3:
        return 0 
        
    return circuit_sizes[0] * circuit_sizes[1] * circuit_sizes[2]

def solve_part2(input_data):
    points = []
    for line in input_data.strip().split('\n'):
        if not line.strip(): continue
        x, y, z = map(int, line.strip().split(','))
        points.append((x, y, z))

    n = len(points)
    pairs = []
    
    # Calculate all pairwise distances
    for i in range(n):
        for j in range(i + 1, n):
            p1 = points[i]
            p2 = points[j]
            dist_sq = (p1[0]-p2[0])**2 + (p1[1]-p2[1])**2 + (p1[2]-p2[2])**2
            pairs.append((dist_sq, i, j))

    pairs.sort(key=lambda x: x[0])
    
    parent = list(range(n))
    size = [1] * n
    num_components = n

    def find(i):
        if parent[i] == i:
            return i
        parent[i] = find(parent[i])
        return parent[i]

    def union(i, j):
        root_i = find(i)
        root_j = find(j)
        if root_i != root_j:
            if size[root_i] < size[root_j]:
                root_i, root_j = root_j, root_i
            parent[root_j] = root_i
            size[root_i] += size[root_j]
            return True
        return False

    for dist, u, v in pairs:
        if union(u, v):
            num_components -= 1
            if num_components == 1:
                return points[u][0] * points[v][0]
                
    return 0

def test():
    example_input = """162,817,812
57,618,57
906,360,560
592,479,940
352,342,300
466,668,158
542,29,236
431,825,988
739,650,466
52,470,668
216,146,977
819,987,18
117,168,530
805,96,715
346,949,466
970,615,88
941,993,340
862,61,35
984,92,344
425,690,689"""
    result = solve(example_input, 10)
    print(f"Part 1 Example result: {result}")
    assert result == 40, f"Expected 40, got {result}"
    
    result_p2 = solve_part2(example_input)
    print(f"Part 2 Example result: {result_p2}")
    assert result_p2 == 25272, f"Expected 25272, got {result_p2}"

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        test()
    else:
        # Resolve path issues by assuming script is run from project root or correct relative path
        try:
            with open("8/input.txt", "r") as f:
                content = f.read()
        except FileNotFoundError:
             # Try absolute path or just assume input is in same dir if running directly
             import os
             input_path = os.path.join(os.path.dirname(__file__), "input.txt")
             with open(input_path, "r") as f:
                content = f.read()
                
        print(f"Part 1: {solve(content, 1000)}")
        print(f"Part 2: {solve_part2(content)}")
